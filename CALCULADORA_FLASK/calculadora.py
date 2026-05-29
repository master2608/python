import math
from flask import render_template, request

def calcular():
    num1_valor = request.form.get("num1", "").strip()
    operacao = request.form.get("operacao")

    if not num1_valor and operacao != "bhaskara":
        return render_template("calculadora.html", etapas="Informe o primeiro número.", resultado="")

    num1 = float(num1_valor) if num1_valor else 0.0

    if operacao == "sqrt":
        if num1 < 0:
            resultado = "Erro: número negativo"
            etapas = f"Não existe raiz real de {num1}."
        else:
            resultado = math.sqrt(num1)
            etapas = f"√{num1} = {resultado}"

    elif operacao == "bhaskara":
        try:
            a = num1
            b = float(request.form.get("num2", 0))
            c = float(request.form.get("num3", 0))

            if a == 0:
                resultado = "Erro"
                etapas = "O coeficiente 'a' não pode ser zero em uma equação de 2º grau."
            else:
                delta = (b ** 2) - (4 * a * c)
                etapas_base = f"Δ = ({b})² - 4 * {a} * {c} = {delta}<br>"

                if delta < 0:
                    resultado = "Sem raízes reais"
                    etapas = etapas_base + "Como Δ é negativo, a equação não possui raízes reais."
                elif delta == 0:
                    x = -b / (2 * a)
                    resultado = f"x = {x}"
                    etapas = etapas_base + f"x = -({b}) / (2 * {a}) = {x}"
                else:
                    x1 = (-b + math.sqrt(delta)) / (2 * a)
                    x2 = (-b - math.sqrt(delta)) / (2 * a)
                    resultado = f"x₁ = {x1} | x₂ = {x2}"
                    etapas = etapas_base + f"x₁ = (-({b}) + √{delta}) / (2 * {a}) = {x1}<br>x₂ = (-({b}) - √{delta}) / (2 * {a}) = {x2}"
        except ValueError:
            return render_template("calculadora.html", etapas="Preencha os coeficientes A, B e C corretamente.", resultado="")

    else:
        num2_valor = request.form.get("num2", "").strip()
        if not num2_valor:
            return render_template(
                "calculadora.html",
                etapas="Informe o segundo número para esta operação.",
                resultado="",
            )
        num2 = float(num2_valor)

        if operacao == "+":
            resultado = num1 + num2
            etapas = f"{num1} + {num2} = {resultado}"
        elif operacao == "-":
            resultado = num1 - num2
            etapas = f"{num1} - {num2} = {resultado}"
        elif operacao == "/":
            if num2 == 0:  
                resultado = "Erro"
                etapas = "Não é possível dividir por zero"
            else:
                resultado = num1 / num2
                etapas = f"{num1} / {num2} = {resultado}"
        elif operacao == "*":
            resultado = num1 * num2
            etapas = f"{num1} * {num2} = {resultado}"
        elif operacao == "**":
            resultado = num1 ** num2
            etapas = f"{num1} ** {num2} = {resultado}"
        elif operacao == "log":
            if num1 <= 0 or num2 <= 0 or num2 == 1:
                resultado = "Erro"
                etapas = "O logaritmando e a base devem ser maiores que zero, e a base deve ser diferente de 1."
            else:
                resultado = math.log(num1, num2)
                etapas = f"log de {num1} na base {num2} = {resultado}"
        else:
            resultado = "Erro"
            etapas = "Operação inválida ou desconhecida."
            
    return render_template('calculadora.html', etapas=etapas, resultado=resultado)
