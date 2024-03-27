import glob
import json
import multiprocessing
import reprlib
import shutil
import subprocess
import sys
import os
import itertools
import tempfile
import time
import traceback
import zmq
from functools import partial
from pathlib import Path
from tqdm import tqdm
from distutils.util import strtobool
import datetime
import argparse
import psycopg2
from multiprocessing.pool import ThreadPool, Pool
from crawl.pruner import Pruner
from subprocess import CalledProcessError, TimeoutExpired




class Tee(object):
    def __init__(self, filename, name):
        self.file = open(f"{filename}-{name}", 'a')
        self.stdout = sys.stdout
        self.name = name

    def __enter__(self):
        sys.stdout = self
        return self.file

    def __exit__(self, exc_type, exc_value, tb):
        sys.stdout = self.stdout
        if exc_type is not None:
            self.file.write(traceback.format_exc())
        self.file.close()

    def write(self, data):
        if data != "\n" and data != " " and data != "":
            data = f"{self.name}: {data}"
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.file.flush()
        self.stdout.flush()



def setup_database():
    """Setup database"""

    # Create db if not exist
    p = subprocess.Popen(["createdb"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if p.returncode != 0:
        test_string = "已经存在"
        if test_string in error.decode("utf-8",errors='replace'):
            # print("error_decode:")
            # print(error)
            print("DB already exists, continue")
        else:
            print(error)
            raise Exception(error,errors='replace')

    # Create table if not exist
    conn = psycopg2.connect()
    cursor = conn.cursor()
    create_table = """CREATE TABLE IF NOT EXISTS accept (
                      id serial PRIMARY KEY,
                      site text NOT NULL,
                      rank int NOT NULL,
                      browser text NOT NULL,
                      version text NOT NULL,
                      clicked_count int NOT NULL,
                      clicked JSONB NOT NULL,
                      locator_count int NOT NULL,
                      unique_locators int NOT NULL,
                      locators JSONB NOT NULL,
                      cookies_before JSONB NOT NULL,
                      cookies_after JSONB NOT NULL,
                      cookies_new JSONB NOT NULL,
                      cookies_removed JSONB NOT NULL,
                      cookies_changed JSONB NOT NULL,
                      error TEXT NOT NULL,
                      insertion_time timestamp NOT NULL DEFAULT current_timestamp(0)
                     )"""
    cursor.execute(create_table)

    create_index = """CREATE INDEX IF NOT EXISTS site_index on accept (site)"""
    cursor.execute(create_index)


    create_table = """CREATE TABLE IF NOT EXISTS responses (
                      id serial PRIMARY KEY,
                      site text NOT NULL,
                      url text NOT NULL,
                      state text NOT NULL,
                      req_headers JSONB NOT NULL,
                      resp_code int NOT NULL,
                      resp_headers JSONB NOT NULL,
                      resp_body_hash text NOT NULL,
                      resp_body_info text NOT NULL,
                      frames int NOT NULL,
                      error_text text NOT NUll,                                            
                      insertion_time timestamp NOT NULL DEFAULT current_timestamp(0)
                     )"""
    cursor.execute(create_table)

    create_index = """CREATE INDEX IF NOT EXISTS site_index on responses (site)"""
    cursor.execute(create_index)

    create_table = """CREATE TABLE IF NOT EXISTS site (
                      id serial PRIMARY KEY,
                      rank int NOT NULL,
                      site text NOT NULL,
                      urls JSONB NOT NULL,
                      crawl_urls JSONB NOT NULL,
                      timeout_crawl bool NOT NULL DEFAULT false,
                      error text NOT NULL DEFAULT '',
                      error_py text NOT NULL DEFAULT  '',                     
                      crawled_urls JSONB NOT NULL DEFAULT '[]',
                      after_basic JSONB NOT NULL DEFAULT '[]',
                      after_trees JSONB NOT NULL DEFAULT '{}',
                      after_trees_limit JSONB NOT NULL DEFAULT '{}',
                      actual_urls JSONB NOT NULL DEFAULT  '{}',
                      insertion_time timestamp NOT NULL DEFAULT current_timestamp(0),
                      confirmed_urls JSONB NOT NULL DEFAULT '{}',
                      timeout_dyn bool NOT NULL DEFAULT false,
                      finished bool NOT NULL DEFAULT false,
                      login_urls JSONB
                    )"""
    cursor.execute(create_table)

    create_index = """CREATE INDEX IF NOT EXISTS site_index on site (site)"""
    cursor.execute(create_index)

    create_table = """CREATE TABLE IF NOT EXISTS dyn_conf (
                      id serial PRIMARY KEY,
                      browser text NOT NULL,
                      version text NOT NULL,
                      site text NOT NULL,
                      opg_url text NOT NULL,
                      url text NOT NULL,
                      inc_method text NOT NULL,
                      state text NOT NULL,
                      run int NOT NULL,
                      observation JSONB NOT NULL,
                      error bool NOT NULL,
                      notes TEXT NOT NULL,
                      response JSONB NOT NULL,                       
                      insertion_time timestamp NOT NULL DEFAULT current_timestamp(0)
                      )"""
    cursor.execute(create_table)

    create_index = """CREATE INDEX IF NOT EXISTS site_index on dyn_conf (site)"""
    cursor.execute(create_index)

    conn.commit()
    conn.close()



#运行命令
def run_cmd(cmd_list, timeout=3600, stdout=sys.stdout, stderr=sys.stderr):
    cmd = []
    [cmd.append(val) for val in cmd_list]
    proc = subprocess.Popen(cmd, stdout=stdout, stderr=stderr)
    try:
        proc.communicate(timeout=timeout)
        if proc.returncode != 0:
            raise CalledProcessError(proc.returncode, "node")
    except TimeoutExpired as e:
        proc.terminate()
        proc.wait(timeout=30)
        raise e




#运行站点检测
def run_site(param):
    rank = str(param[0])
    site = param[1]
    try:
        run_cmd(["node", "crawl/acceptor_test.js", site, rank, str(args.button_timeout), str(args.load_timeout)])
    except CalledProcessError:
        print(f"{site} failed")




#返回加载时间
def path_age(path):
    return time.time() - os.path.getmtime(path)


def clean_up(args):
    # Remove old directories
    # playwright_dirs = glob.glob("/tmp/playwright*")
    # playwright_dirs.extend(glob.glob("/tmp/Temp-*"))
    # playwright_dirs.extend(glob.glob("/tmp/.org.chromium.*"))
    playwright_dirs = (
            glob.glob("/tmp/playwright*")
            + glob.glob("/tmp/Temp-*")
            + glob.glob("/tmp/.org.chromium.*")
    )
    for playwright_dir in playwright_dirs:
        try:
            age = path_age(playwright_dir)
            if age > (1.02 * args.dyn_timeout):
                # print(f"Remove old dir: {playwright_dir}")
                shutil.rmtree(playwright_dir, ignore_errors=True)
                Path(playwright_dir).unlink(missing_ok=True)
        except Exception as e:
            pass
            # print(f"Remove dir error: {e}")
    kill_old_processes_windows(args)



def kill_old_processes_windows(args):
    """Kills old Playwright processes on Windows."""

    tasklist_command = ["tasklist", "/FI", "IMAGENAME eq node.exe"]  # List processes
    taskkill_command = ["taskkill", "/F", "/PID", "%s"]  # Kill processes

    processes_to_check = [
        ("node crawl/dil.js", args.coll_timeout),
        ("node crawl/dyn.js", args.dyn_timeout),
    ]

    for process_name, timeout in processes_to_check:
        try:
            output = subprocess.check_output(tasklist_command).decode("utf-8")
            matches = [line for line in output.splitlines() if process_name in line]

            for match in matches:
                pid = int(match.split()[1])  # Extract PID from tasklist output
                current_time = time.time()

                # Get process creation time using WMI (Windows Management Instrumentation)
                process_creation_time = _get_process_creation_time(pid)

                time_running_in_seconds = current_time - process_creation_time
                if time_running_in_seconds > timeout * 1.02:
                    try:
                        subprocess.check_call(taskkill_command % pid)  # Kill the process
                    except Exception as e:
                        pass  # Handle any errors during killing
        except Exception as e:
            pass  # Handle errors during process listing or killing

# Helper function to get process creation time using WMI
def _get_process_creation_time(pid):
    c = wmi.WMI()
    for process in c.Win32_Process(ProcessId=pid):
        return process.CreationDate.timestamp()

def run_dil(param):
    global pruner
    rank = str(param[0])
    site = param[1]
    args = param[2]
    name = multiprocessing.current_process().name
    if args.mode == "dil-login":
        login = "True"
    else:
        login = ""

    with Tee(f"log/{args.mode}-{args.PGDATABASE}.log", name) as f:
        # Remove old directories and kill old processes
        clean_up(args)

        # 1.Collect URLs + 2. Collect responses
        if args.run_node:
            try:
                run_cmd(["node", "crawl/dil.js", site, rank, ignoreHTTPSErrors, str(args.load_timeout),
                         str(args.button_timeout), str(args.limit_crawl), login], args.coll_timeout, stdout=f, stderr=f)
            except (CalledProcessError, OSError) as e:
                pruner.update("UPDATE site SET error_py = %s WHERE site = %s", (f"col-{str(e)}", site,))
                print(f"{site} failed: collect URLs or collect responses")
            except TimeoutExpired:
                pruner.update("UPDATE site SET timeout_crawl = TRUE WHERE site = %s", (site,))
                print(f"{site} timeout: collect URLs or collect responses")

            # 3. Pruning and stuff
            # Get urls + basic pruning
            try:
                input_rows, basic_pruned = pruner.get_urls(site)
            except Exception as e:
                pruner.update("UPDATE site SET error_py = error_py || E'\n' || %s , finished = TRUE WHERE site = %s",
                              (f"get-{str(e)}", site,))
                print(f"{site} error in get_urls: {e}, abort")
                return
            if len(input_rows) == 0:
                return
            # Advanced (tree) pruning
            try:
                urls = pruner.predict_trees(input_rows, site)
            except Exception as e:
                pruner.update("UPDATE site SET error_py = error_py || E'\n' || %s , finished = TRUE WHERE site = %s",
                              (f"pred-{str(e)}", site,))
                print(f"{site} error in predict_trees: {e}, abort")
                return
            print(reprlib.repr(urls))
            if len(urls) == 0:
                return

            """
            urls = {
                "img": {"https://google.com/": "cfw"},  #, "https://google.com/search/": "c"},
                "iframe": {"https://google.com/": "f"}
            }
            """

            # 4. Dynamic confirmation
            # Test all inc-url-browser pairs that might work in the correct states

            # Limit if wanted
            if args.limit_conv:
                for inc_method, entries in urls.items():
                    urls[inc_method] = dict(itertools.islice(entries.items(), args.limit_conv))

            pruner.update("UPDATE site SET after_trees_limit =  %s WHERE site = %s",(json.dumps(urls), site,))

            # Test every URL that should be tested in one of both browsers according to the trees in both
            # This makes sure that not the trees are responsible for one URL only being vulnerable in one browser
            actual_urls = {}
            for inc, vals in urls.items():
                new_vals = {}
                for u, _ in vals.items():
                    new_vals[u] = "cf"
                actual_urls[inc] = new_vals

            pruner.update("UPDATE site SET actual_urls = %s WHERE site = %s",(json.dumps(actual_urls), site,))

            # Test up to 5 times
            # Always test all three states (if possible, try state creation again + early abort again),
            # (even if trees only say two states are distinguishable)
            try:
                run_cmd(["node", "crawl/dyn.js", site, rank, json.dumps(actual_urls), ignoreHTTPSErrors, str(args.load_timeout),
                         str(args.button_timeout), login], args.dyn_timeout, stdout=f, stderr=f)
            # List of URLs can get large:
            # Increase system limits: https://unix.stackexchange.com/a/45584
            except (CalledProcessError, OSError) as e:
                pruner.update("UPDATE site SET error_py = error_py || E'\n' || %s  WHERE site = %s", (f"dyn-{str(e)}", site,))
                print(f"{site} failed: dynamic confirmation")
            except TimeoutExpired:
                pruner.update("UPDATE site SET timeout_dyn = TRUE WHERE site = %s", (site,))
                print(f"{site} timeout: dynamic confirmation")

        # 5. Process results (which URLs were distinguishable)
        # The same observation property has to be different in all 5 runs for a state-pair to be counted
        try:
            pruner.get_confirmed(site)
        except Exception as e:
            pruner.update("UPDATE site SET error_py = error_py || E'\n' || %s , finished = TRUE WHERE site = %s",
                          (f"conf-{str(e)}", site,))
            print(f"{site} error in get_confirmed: {e}")


ignoreHTTPSErrors = ""  # "" (empty string) for false, "True" for True
pruner = None


def setup_pruner(args):
    global pruner
    name = multiprocessing.current_process().name
    # num = int(name.rsplit("-", maxsplit=1)[1]) - 1
    split_result = name.rsplit("-", maxsplit=1)
    num = int(split_result[1]) - 1 if len(split_result) > 1 else 0
    time.sleep(num * 5)  # Slowly start all processes, one new every 5 seconds
    with Tee(f"log/{args.mode}-{args.PGDATABASE}.log", name):
        pruner = Pruner(args.tree_glob)


def main(args):
    # Better logging
    Path("log").mkdir(exist_ok=True)
    with Tee(f"log/{args.mode}-{args.PGDATABASE}.log", "main"):
        # Database setup
        os.environ["PGHOST"] = args.PGHOST
        os.environ["PGUSER"] = args.PGUSER
        os.environ["PGDATABASE"] = args.PGDATABASE
        os.environ["PGPASSWORD"] = args.PGPASSWORD
        os.environ["PGPORT"] = args.PGPORT

        if args.site !="":
            sites=[args.site]
        elif args.sites_file!="":
            sites=open(args.sites_file).read().splitlines()

        if args.mode == "codegen":
            # df = pd.DataFrame({"sites": top_100, "accept": ["" for _ in range(100)], "notes": ["" for _ in range(100)]})
            # df.to_csv("top_100.csv")
            for site in sites:
                try:
                    subprocess.check_call(
                        ["C:/Users/35093/AppData/Roaming/npm/npx.cmd", "playwright", "codegen", "--browser", "firefox", site, "--timeout", "30000"])
                except CalledProcessError:
                    print(f"{site} failed")
        elif args.mode == "test":
            setup_database()
            with ThreadPool(args.pool) as tp:
                # r = list(tqdm(tp.imap(run_site, enumerate(sites)), position=0, leave=True, desc="Run"))
                r = list(tqdm(tp.imap(partial(run_site, args=args), enumerate(sites)), position=0, leave=True, desc="Run"))
        elif args.mode.startswith("dil"):
            setup_database()
            temp_h2o_root = tempfile.mkdtemp(prefix='h2o_root_')
            with open(os.devnull, 'w') as devnull:
                jar_path = f"D:/code/python/python-3.11/Lib/site-packages/h2o/backend/bin/h2o.jar"
                proc = subprocess.Popen(
                    ["java", "-ea", "-Xmx50G", "-jar", jar_path, "-ip", "127.0.0.1", "-web_ip", "127.0.0.1",
                     "-baseport", "54321", "-ice_root", temp_h2o_root,
                     "-nthreads", "75", "-log_level", "FATA", "-name",
                     "H2O_from_python_dil", "-allow_unsupported_java"],
                    stdout=devnull, stderr=devnull)
                try:
                    print(proc.pid)
                    time.sleep(10)
                    initial_pruner = Pruner(args.tree_glob, initial=True)
                    with Pool(args.pool, initializer=setup_pruner, initargs=(args,)) as p:
                        if args.mode == "dil":
                            # r = list(tqdm(p.imap(partial(run_dil, args=args),[(rank + args.t_start, site) for rank, site in enumerate(sites)]),position=0, leave=True, desc="Dil"))
                            r = list(tqdm(p.imap(run_dil, [[rank + args.t_start, site, args] for rank, site in enumerate(sites)]), position=0, leave=True, desc="Dil"))
                        elif args.mode == "dil-login":
                            # Listen to incoming zeromq messages
                            # start run_dil (rank, site, args) when message comes in
                            # Stop listening when "End" command is send (current processes can still finish)
                            context = zmq.Context()
                            socket = context.socket(zmq.REP)
                            socket.bind("tcp://127.0.0.1:5555")
                            cont = True
                            print("Ready to receive messages!")
                            while cont:
                                site = socket.recv_string()
                                if site == "End":
                                    cont = False
                                    socket.send_string("Ack")
                                elif site == "Free":
                                    free = args.pool - len(p._cache)
                                    socket.send_string(f"{free}")
                                else:
                                    # rank = t_list.rank(site)
                                    print(f"Start: {site}, {0}")
                                    p.imap(run_dil, [[0, site,  args]])
                                    free = args.pool - len(p._cache)
                                    socket.send_string(f"{free}")

                            p.close()
                            p.join()
                        else:
                            print(f"Mode: {args.mode} is not supported!")
                except Exception as e:
                    print(e)
                    print(f"Error: {e}")
                finally:
                    proc.terminate()
                    temp_h2o_root = tempfile.mkdtemp(prefix='h2o_root_')
                    shutil.rmtree(temp_h2o_root)

        else:
            print(f"Mode: {args.mode} is not supported!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Other settings
    parser.add_argument("--mode", type=str, default="test",
                        help="Mode: one of 'codegen', 'test', 'dil', 'dil-login'.")

    # Tranco settings
    parser.add_argument("--t_date", type=datetime.date.fromisoformat, default="2022-04-24",
                        help="Date of the tranco list to pull.")
    parser.add_argument("--sites_file", type=str, default="",
                        help="Path to sites_file, will be used instead of tranco.")
    parser.add_argument("--site", type=str, default="",
                        help="Name of a single site, will be used instead of tranco.")
    parser.add_argument("--t_start", type=int, default=0,
                        help="First tranco rank to use.")
    parser.add_argument("--t_end", type=int, default=100,
                        help="Last tranco rank to use.")

    # Test mode settings
    parser.add_argument("--pool", type=int, default=10,
                        help="How many browsers to start in parallel (for test and dil mode).")
    parser.add_argument("--button_timeout", type=int, default=10000,
                        help="Timeout for looking for buttons in ms.")
    parser.add_argument("--load_timeout", type=int, default=30000,
                        help="Timeout for page load (load event fired) in ms.")

    # Dil mode settings
    parser.add_argument("--limit_conv", type=int, default=25,
                        help="Maximum number of URLs for one inclusion method to test.")
    parser.add_argument("--limit_crawl", type=int, default=500,
                        help="Maximum number of URLs that get crawled in the initial response collection phase (doubled for dil-login).")
    parser.add_argument("--tree_glob", type=str, default="mojo/*.mojo",
                        help="Glob pattern to load the mojo files.")
    parser.add_argument("--coll_timeout", type=int, default=3600,
                        help="Maximum time in seconds responses are collected on a site")
    parser.add_argument("--dyn_timeout", type=int, default=10800,
                        help="Maximum time in seconds dynamic confirmation runs on a site")
    parser.add_argument("--run_node", type=lambda x: bool(strtobool(str(x))), default=True,
                        help="Whether to run node.js code in dil-mode or only the final python code.")

    # Database settings
    parser.add_argument("--PGHOST", type=str, default="localhost",
                        help="Postgres host")
    parser.add_argument("--PGUSER", type=str, default=os.environ.get("USER"),
                        help="Postgres user")
    parser.add_argument("--PGDATABASE", type=str, default=os.environ.get("USER"),
                        help="Database to use")
    parser.add_argument("--PGPASSWORD", type=str, default="",
                        help="PW of postgres user")
    parser.add_argument("--PGPORT", type=str, default="5432",
                        help="Port of postgres instance")

    args = parser.parse_args()
    main(args)
