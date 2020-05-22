from flask import Flask, render_template, request, redirect, session
import Hwang_Adegbite_Urbina_benaloh
import pymysql.cursors
import hashlib

app = Flask(__name__)
app.secret_key = b'\xe6\x12nL\xb1\xc1\xf9\x00_;|\xfe}\xfc^\x17'
conn = pymysql.connect(host="localhost",
                       port=3306,
                       user="root",
                       password="root",
                       db="project",
                       charset="utf8mb4",
                       cursorclass=pymysql.cursors.DictCursor)
benaloh_public_key = -1
benaloh_private_key = -1


@app.route("/")
def home():
    global benaloh_public_key, benaloh_private_key
    if benaloh_public_key == -1:
        (benaloh_public_key, benaloh_private_key) = Hwang_Adegbite_Urbina_benaloh.gen(5)
    return render_template("home.html")


@app.route("/voter_portal", methods=["GET", "POST"])
def voter_portal():
    if request.method == "POST":
        voter_id = request.form["ID"]
        hash_id = hashlib.sha256(voter_id.encode("utf-8")).hexdigest()
        try:
            with conn.cursor() as cursor:
                query = "INSERT INTO Voter (ID) VALUES (%s)"
                cursor.execute(query, (hash_id))
                conn.commit()
                session["voter"] = hash_id
        except pymysql.err.IntegrityError:
            return render_template("voter_portal.html", error="You have already voted")
        return redirect("/vote")
    return render_template("voter_portal.html")


@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        vote_int = int(request.form["vote"])
        b_enc_vote = Hwang_Adegbite_Urbina_benaloh.enc(vote_int, benaloh_public_key)
        try:
            with conn.cursor() as cursor:
                b_query = "UPDATE Voter SET b_enc_vote = %s WHERE ID = %s"
                cursor.execute(b_query, (b_enc_vote, session["voter"]))
                conn.commit()
        except Exception as e:
            return render_template("vote.html", error=e)
        return redirect("/")
    return render_template("vote.html")


@app.route("/view_results")
def results():
    enc_sum = 0
    total_votes = 0
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ROUND(EXP(SUM(LOG(b_enc_vote))),1) AS product, COUNT(b_enc_vote) FROM Voter")
            result = cursor.fetchone()
            enc_sum += int(result["product"])
            total_votes += int(result["COUNT(b_enc_vote)"])
    except Exception as e:
        return render_template("view_results.html", error=e)

    dec_sum = Hwang_Adegbite_Urbina_benaloh.dec(enc_sum, benaloh_private_key, benaloh_public_key)
    b_votes = dec_sum
    a_votes = total_votes - b_votes
    return render_template("view_results.html", b_votes=b_votes, a_votes=a_votes)


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
