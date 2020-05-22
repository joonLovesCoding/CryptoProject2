import Hwang_Adegbite_Urbina_benaloh
import timeit


def driver(trials):
    total_time = 0
    total_correct = 0

    for i in range(trials):
        start = timeit.default_timer()
        pk, sk = Hwang_Adegbite_Urbina_benaloh.gen(5)
        m1 = 1
        m2 = 1
        m3 = 0
        m4 = 0
        c1 = Hwang_Adegbite_Urbina_benaloh.enc(m1, pk)
        c2 = Hwang_Adegbite_Urbina_benaloh.enc(m2, pk)
        c3 = Hwang_Adegbite_Urbina_benaloh.enc(m3, pk)
        c4 = Hwang_Adegbite_Urbina_benaloh.enc(m4, pk)
        if Hwang_Adegbite_Urbina_benaloh.dec(c1 * c2 * c3 * c4, sk, pk) == 2:
            total_correct += 1

        stop = timeit.default_timer()
        total_time += stop - start

    print(f"Trials: {trials}\nBenaloh % correctness: {(total_correct/trials) * 100}%\n"
          f"Average runtime: {total_time/trials}")


driver(1000)
