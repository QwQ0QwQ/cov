import ast
def main():
    try:
        with open("input.txt", "r",encoding="utf-8-sig") as file:
            js_obj = file.read()
            ast.literal_eval(js_obj)
            print(py_obj)
    except FileNotFoundError:
        print("File not found.")
    except SyntaxError:
        print("Invalid JSON syntax.")

if __name__ == "__main__":
    main()
