import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


HTML = """
<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DanialTool</title>

<style>
body {
    background: #111;
    color: white;
    font-family: Arial, sans-serif;
    padding: 20px;
}

.container {
    max-width: 600px;
    margin: auto;
}

h1 {
    color: #00ffff;
}

.option {
    padding: 12px;
    margin: 8px 0;
    border-radius: 10px;
    background: #222;
}

input, select, button {
    width: 100%;
    padding: 12px;
    margin-top: 8px;
    margin-bottom: 12px;
    border-radius: 8px;
    border: none;
    box-sizing: border-box;
}

button {
    background: #00aaaa;
    color: white;
    font-size: 16px;
}

.result {
    background: #222;
    padding: 15px;
    border-radius: 10px;
    white-space: pre-wrap;
}
</style>
</head>

<body>

<div class="container">

<h1>Salam DADASHI!</h1>

<p>
Az in barname mitooni baraye taghalob ya abzare komaki, estefade koni.
</p>

<div class="option">1. bakhsh paziri</div>
<div class="option">2. zoj ya fard</div>
<div class="option">3. adade avval</div>
<div class="option">4. baghi mande va khareje ghesmate taghsim</div>
<div class="option">5. jadval zarb ( adad ro to midi )</div>
<div class="option">6. miangin nomrehat chande? ( moaddel )</div>

<form method="POST">

<label>Adade gozinei ke mikhay ro benevis :</label>

<select name="entekhab">
    <option value="1">1. bakhsh paziri</option>
    <option value="2">2. zoj ya fard</option>
    <option value="3">3. adade avval</option>
    <option value="4">4. baghi mande va khareje ghesmate taghsim</option>
    <option value="5">5. jadval zarb</option>
    <option value="6">6. miangin</option>
</select>

<div id="inputs">

<label>Adad ra vared konid :</label>
<input type="number" name="number">

</div>

<button type="submit">Ejra</button>

</form>

<div class="result">
RESULT
</div>

</div>

<script>

const select = document.querySelector("select");
const inputs = document.getElementById("inputs");

function changeInputs() {

    let choice = select.value;

    if (choice == "1" || choice == "2" || choice == "3" || choice == "5") {

        inputs.innerHTML =
        '<label>Adad ra vared konid :</label>' +
        '<input type="number" name="number">';

    }

    if (choice == "4") {

        inputs.innerHTML =
        '<label>Adade aval ra vared konid:</label>' +
        '<input type="number" name="number4">' +

        '<label>Adade dovom ra vared konid:</label>' +
        '<input type="number" name="number5">';

    }

    if (choice == "6") {

        inputs.innerHTML =
        '<label>Chand ta nomre darid? ( tedade nomarat )</label>' +
        '<input type="number" name="tedad" min="1">' +

        '<p>بعد از زدن Ejra، قسمت وارد کردن نمره‌ها ظاهر می‌شود.</p>';

    }
}

select.addEventListener("change", changeInputs);

</script>

</body>
</html>
"""


class DanialTool(BaseHTTPRequestHandler):

    def do_GET(self):

        page = HTML.replace(
            "RESULT",
            "Result inja namayesh dade mishe."
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(page.encode("utf-8"))

    def do_POST(self):

        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode("utf-8")
        form = parse_qs(data)

        entekhab = form.get("entekhab", [""])[0]

        result = ""

        # 1
        if entekhab == "1":

            number = int(form.get("number", ["0"])[0])

            if number > 10000:

                result = "Lotfan adade zire 10 hezar vared konid"

            else:

                divisors = []

                for x in range(1, 10000):

                    if number % x == 0:

                        divisors.append(
                            str(number) + " bakhsh pazir hast bar " + str(x)
                        )

                result = "\n".join(divisors)

        # 2
        elif entekhab == "2":

            number2 = int(form.get("number", ["0"])[0])

            if number2 % 2 == 0:

                result = str(number2) + " zoj ast"

            else:

                result = str(number2) + " fard ast"

        # 3
        elif entekhab == "3":

            number3 = int(form.get("number", ["0"])[0])

            if number3 < 2:

                result = "Adad avval nist"

            else:

                prime = True

                for x in range(2, number3):

                    if number3 % x == 0:

                        prime = False
                        break

                if prime:

                    result = str(number3) + " adade avval hast"

                else:

                    result = str(number3) + " adade avval nist"

        # 4
        elif entekhab == "4":

            number4 = int(form.get("number4", ["0"])[0])
            number5 = int(form.get("number5", ["1"])[0])

            khareje_ghesmat = number4 // number5
            baghimande = number4 % number5

            result = (
                "Khareje ghesmat: " + str(khareje_ghesmat) +
                "\nBaghimande: " + str(baghimande)
            )

        # 5
        elif entekhab == "5":

            number5 = int(form.get("number", ["0"])[0])

            lines = []

            for x in range(1, 51):

                lines.append(
                    str(number5) + " x " +
                    str(x) + " = " +
                    str(number5 * x)
                )

            result = "\n".join(lines)

        # 6
        elif entekhab == "6":

            tedad = int(form.get("tedad", ["0"])[0])

            result = (
                "Chand ta nomre darid? ( tedade nomarat )\n"
                "Tedade nomarat: " + str(tedad) +
                "\n\nبرای نسخه بعدی می‌تونیم وارد کردن تک‌تک نمره‌ها رو هم اضافه کنیم."
            )

        page = HTML.replace("RESULT", result)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(page.encode("utf-8"))


port = int(os.environ.get("PORT", 10000))

server = HTTPServer(("0.0.0.0", port), DanialTool)

print("DanialTool is running on port", port)

server.serve_forever()
