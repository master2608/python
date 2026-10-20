
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard de Vendas de Carros",
    page_icon="🚗",
    layout="wide"
)

CATALOGO = {
    "Fiat Argo 1.0": {
        "marca": "Fiat",
        "ano": 2025,
        "preco": 85000.00
    },
    "Chevrolet Onix 1.0": {
        "marca": "Chevrolet",
        "ano": 2025,
        "preco": 92000.00
    },
    "Volkswagen Polo 1.0": {
        "marca": "Volkswagen",
        "ano": 2025,
        "preco": 95000.00
    },
    "Hyundai HB20 1.0": {
        "marca": "Hyundai",
        "ano": 2025,
        "preco": 89000.00
    },
    "Toyota Corolla 2.0": {
        "marca": "Toyota",
        "ano": 2024,
        "preco": 155000.00
    },
    "Honda Civic 2.0": {
        "marca": "Honda",
        "ano": 2024,
        "preco": 180000.00
    },
    "Jeep Compass 1.3": {
        "marca": "Jeep",
        "ano": 2025,
        "preco": 175000.00
    },
    "BYD Dolphin": {
        "marca": "BYD",
        "ano": 2025,
        "preco": 150000.00
    }
}

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if "vendas" not in st.session_state:
    st.session_state.vendas = []

st.title("Dashboard de Vendas de Carros")
st.markdown("---")

st.subheader("Resumo da Concessionária")

total_vendido = sum(
    venda["Total (R$)"] for venda in st.session_state.vendas
)

total_vendas = len(st.session_state.vendas)

carros_vendidos = sum(
    venda["Quantidade"] for venda in st.session_state.vendas
)

col1, col2, col3 = st.columns(3)

col1.metric("Faturamento Total", f"R$ {total_vendido:,.2f}")
col2.metric("Vendas Realizadas", total_vendas)
col3.metric("Carros Vendidos", carros_vendidos)

st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Catálogo de Veículos")

    with st.form("form_carro"):
        carro_nome = st.selectbox(
            "Selecione o veículo",
            list(CATALOGO.keys())
        )

        carro = CATALOGO[carro_nome]

        st.write(f"**Marca:** {carro['marca']}")
        st.write(f"**Ano:** {carro['ano']}")
        st.caption(f"Preço unitário: R$ {carro['preco']:,.2f}")

        quantidade = st.number_input(
            "Quantidade",
            min_value=1,
            value=1,
            step=1
        )

        desconto = st.number_input(
            "Desconto por carro (R$)",
            min_value=0.0,
            max_value=float(carro["preco"]),
            value=0.0,
            step=500.0
        )

        adicionar = st.form_submit_button(
            "Adicionar ao Carrinho",
            use_container_width=True
        )

        if adicionar:
            subtotal = (carro["preco"] - desconto) * quantidade

            st.session_state.carrinho.append({
                "Veículo": carro_nome,
                "Marca": carro["marca"],
                "Ano": carro["ano"],
                "Preço Unit. (R$)": carro["preco"],
                "Quantidade": quantidade,
                "Desconto Unit. (R$)": desconto,
                "Subtotal (R$)": subtotal
            })

            st.success(f"{carro_nome} adicionado com sucesso!")

    st.subheader("Carrinho de Vendas")

    if st.session_state.carrinho:
        df_carrinho = pd.DataFrame(st.session_state.carrinho)

        st.dataframe(
            df_carrinho,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Preço Unit. (R$)": st.column_config.NumberColumn(
                    "Preço Unitário",
                    format="R$ %.2f"
                ),
                "Desconto Unit. (R$)": st.column_config.NumberColumn(
                    "Desconto por Carro",
                    format="R$ %.2f"
                ),
                "Subtotal (R$)": st.column_config.NumberColumn(
                    "Subtotal",
                    format="R$ %.2f"
                )
            }
        )

        total_compra = sum(
            item["Subtotal (R$)"]
            for item in st.session_state.carrinho
        )

        st.metric("Total da Venda", f"R$ {total_compra:,.2f}")

        if st.button("Limpar Carrinho", use_container_width=True):
            st.session_state.carrinho = []
            st.rerun()

    else:
        st.info("O carrinho está vazio. Selecione um veículo acima.")

with col2:
    st.subheader("Pagamento e Fechamento")

    total_compra = sum(
        item["Subtotal (R$)"]
        for item in st.session_state.carrinho
    )

    st.metric(
        label="TOTAL A PAGAR",
        value=f"R$ {total_compra:,.2f}"
    )

    st.markdown("---")

    forma_pagamento = st.selectbox(
        "Forma de pagamento",
        [
            "À vista",
            "Financiamento",
            "Cartão de crédito",
            "PIX"
        ]
    )

    with st.form("form_pagamento"):
        cliente = st.text_input("Nome do cliente")

        valor_recebido = st.number_input(
            "Valor recebido (R$)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            format="%.2f"
        )

        finalizar = st.form_submit_button(
            "Finalizar Venda",
            type="primary",
            use_container_width=True
        )

        if finalizar:
            if not st.session_state.carrinho:
                st.warning(
                    "Adicione pelo menos um veículo antes de finalizar."
                )

            elif not cliente.strip():
                st.warning("Informe o nome do cliente.")

            elif valor_recebido < total_compra:
                falta = total_compra - valor_recebido

                st.error(
                    f"Valor insuficiente. Faltam R$ {falta:,.2f}."
                )

            else:
                troco = valor_recebido - total_compra

                venda = {
                    "Cliente": cliente.strip(),
                    "Veículos": ", ".join(
                        item["Veículo"]
                        for item in st.session_state.carrinho
                    ),
                    "Quantidade": sum(
                        item["Quantidade"]
                        for item in st.session_state.carrinho
                    ),
                    "Total (R$)": total_compra,
                    "Forma de Pagamento": forma_pagamento
                }

                st.session_state.vendas.append(venda)
                st.session_state.ultima_venda = {
                    **venda,
                    "Valor Recebido (R$)": valor_recebido,
                    "Troco (R$)": troco
                }
                st.session_state.carrinho = []

                st.success("Venda realizada com sucesso!")

                st.metric("Troco a Devolver", f"R$ {troco:,.2f}")

                st.rerun()

    if "ultima_venda" in st.session_state:
        with st.expander("Ver Comprovante da Última Venda"):
            venda = st.session_state.ultima_venda

            st.write(f"**Cliente:** {venda['Cliente']}")
            st.write(f"**Veículos:** {venda['Veículos']}")
            st.write(f"**Quantidade:** {venda['Quantidade']}")
            st.write(f"**Total:** R$ {venda['Total (R$)']:,.2f}")
            st.write(
                f"**Pagamento:** {venda['Forma de Pagamento']}"
            )
            st.write(
                f"**Valor recebido:** R$ {venda['Valor Recebido (R$)']:,.2f}"
            )
            st.write(f"**Troco:** R$ {venda['Troco (R$)']:,.2f}")

st.markdown("---")

st.subheader("Histórico de Vendas")

if st.session_state.vendas:
    df_vendas = pd.DataFrame(st.session_state.vendas)

    st.dataframe(
        df_vendas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total (R$)": st.column_config.NumberColumn(
                "Valor da Venda",
                format="R$ %.2f"
            )
        }
    )

    st.subheader("Faturamento por Veículo")

    faturamento_carros = {}

    for venda in st.session_state.vendas:
        for item in []:
            pass

    for venda in st.session_state.vendas:
        for nome in venda["Veículos"].split(", "):
            faturamento_carros[nome] = (
                faturamento_carros.get(nome, 0) + 1
            )

    df_carros = pd.DataFrame(
        list(faturamento_carros.items()),
        columns=["Veículo", "Ocorrências nas Vendas"]
    )

    st.bar_chart(
        df_carros.set_index("Veículo")
    )

else:
    st.info("Nenhuma venda foi realizada nesta sessão.")
