import pandas as pd
import base64
from datetime import datetime
from pathlib import Path


def get_logo_b64() -> str:
    for path in ["static/logo.png", "styles/logo.png", "logo.png"]:
        p = Path(path)
        if p.exists():
            with open(p, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return ""


def formatar_brl(valor: float) -> str:
    if pd.isna(valor) or valor == 0:
        return "—"
    valor_reais = valor / 100
    return f"R$ {valor_reais:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def badge(v: float) -> str:
    seta = "&#9650;" if v >= 0 else "&#9660;"
    bg   = "#E8F7EC" if v >= 0 else "#FDEAEA"
    cor  = "#1E7A3C" if v >= 0 else "#C0392B"
    av = abs(v) / 100
    txt = f"{av:,.2f}".replace(",","X").replace(".",",").replace("X",".")
    return (
        f'<span style="display:inline-block;font-size:0.58rem;font-weight:700;'
        f'padding:1px 4px;border-radius:4px;background:{bg};color:{cor};'
        f'white-space:nowrap;max-width:100%;">{seta} {txt}</span>'
    )


# CSS idêntico ao da página original — embutido no HTML para funcionar offline
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@400;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #fff; font-family: 'Source Sans 3', sans-serif; color: #1A0A02; }

.panfleto-page {
    display: grid;
    grid-template-columns: 1fr 1px 1fr;
    gap: 0;
    width: 100%;
    align-items: start;
}
.divisor { width: 1px; background: #E8D5C8; margin: 0 14px; }
.panfleto-col { padding: 0 3px; min-width: 0; }

.pf-header {
    display: flex;
    align-items: center;
    gap: 7px;
    justify-content: center;
    padding-bottom: 5px;
    margin-bottom: 6px;
    border-bottom: 1.5px solid #E8D5C8;
}
.pf-logo {
    width: 26px; height: 26px; flex-shrink: 0;
    background: transparent;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
}
.pf-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 1.20rem;
    font-weight: 700;
    color: #5A1F05;
    margin: 0 0 1px;
    line-height: 1.1;
}
.pf-header p {
    font-size: 0.54rem;
    color: #9E7E6A;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: .07em;
    font-weight: 600;
}

.pf-month {
    margin-bottom: 3px;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #E8D5C8;
}
.pf-month-header {
    background: linear-gradient(90deg, #5A1F05, #7D0911);
    padding: 0px 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 4px;
    flex-wrap: nowrap;
}
.pf-month-header h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.0rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    white-space: nowrap;
}
.pf-pills { display: flex; gap: 3px; flex-wrap: nowrap; }
.pf-pill {
    font-size: 0.65rem;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 20px;
    white-space: nowrap;
}
.pf-pill-r  { background: rgba(255,255,255,.18); color: #fff; }
.pf-pill-d  { background: rgba(255,255,255,.1);  color: rgba(255,255,255,.85); }
.pf-pill-lp { background: #E8F7EC; color: #1E7A3C; }
.pf-pill-ln { background: #FDEAEA; color: #C0392B; }

table.pft {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.75rem;
    table-layout: fixed;
}
table.pft thead tr { background: #FDF6F0; }
table.pft thead th {
    padding: 3px 4px;
    text-align: left;
    font-size: 0.64rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .05em;
    color: #9E7E6A;
    border-bottom: 1.5px solid #E8D5C8;
    white-space: nowrap;
    overflow: hidden;
}
table.pft thead th.r { text-align: right; }
table.pft th:nth-child(4), table.pft td:nth-child(4) { max-width: 80px; overflow: hidden; }
table.pft th:nth-child(1), table.pft td:nth-child(1) { width: 42px; }
table.pft tbody tr  { border-bottom: 1px solid #F0E8E0; }
table.pft tbody tr:nth-child(even) { background: #FDFAF8; }
table.pft tbody td  { padding: 3px 4px; white-space: nowrap; overflow: hidden; color: #1A0A02; }
table.pft tbody td.r  { text-align: right; font-variant-numeric: tabular-nums; }
table.pft tbody td.ch { font-weight: 700; color: #5A1F05; }
table.pft tfoot tr  { background: #5A1F05; }
table.pft tfoot td  {
    padding: 3px 4px;
    font-weight: 700;
    font-size: 0.75rem;
    color: #fff;
    white-space: nowrap;
}
table.pft tfoot td.r { text-align: right; font-variant-numeric: tabular-nums; }

.pf-obs {
    padding: 0px 8px 0px;
    background: #FDF6F0;
    border-top: 1px solid #E8D5C8;
    font-size: 0.62rem;
    line-height: 1.6;
    color: #5A3D2B;
}
.pf-obs-label {
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: #9E7E6A;
    margin-right: 4px;
}

.pf-footer {
    margin-top: 4px;
    padding-top: 3px;
    border-top: 1px solid #E8D5C8;
    font-size: 0.50rem;
    color: #9E7E6A;
    text-align: center;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .05em;
}

@media print {
    @page { size: A4 landscape; margin: 4mm 4mm; }
    body  { margin: 0; padding: 0; }

    table.pft           { font-size: 0.62rem; }
    table.pft thead tr  { background: #ffffff; }
    table.pft thead th  { font-size: 0.59rem; padding: 2px 2px; }
    table.pft tbody td  { padding: 1px 2px; }
    table.pft tfoot td  { padding: 2px 2px; font-size: 0.59rem; }
    .pf-month           { margin-bottom: 4px; border-radius: 4px; }
    .pf-month-header    { padding: 2px 6px; }
    .pf-month-header h2 { font-size: 0.72rem; }
    .pf-pill            { font-size: 0.56rem; padding: 0px 4px; }
    .pf-header          { padding-bottom: 4px; margin-bottom: 5px; }
    .pf-header h1       { font-size: 0.95rem; }
    .pf-logo            { width: 22px; height: 22px; }
    .pf-obs             { font-size: 0.44rem; padding: 1px 5px; background: #ffffff; }
    .pf-footer          { font-size: 0.44rem; margin-top: 3px; padding-top: 2px; }
}
</style>
"""


def build_panfleto(periodos: list, df: pd.DataFrame) -> str:
    """Mesma função da página original — gera o HTML de um panfleto."""
    logo_b64 = get_logo_b64()
    logo_img = (
        f'<img src="data:image/png;base64,{logo_b64}" '
        f'style="width:22px;height:22px;object-fit:contain;">'
        if logo_b64 else ""
    )

    cabecalho = (
        '<div class="pf-header">'
        f'<div class="pf-logo" style="background:transparent;padding:1px;">{logo_img}</div>'
        '<div>'
        '<h1>Relatório Financeiro IBF</h1>'
        '</div>'
        '</div>'
    )

    blocos = ""
    for ano, mes, label in periodos:
        df_mes = df[(df["Ano"] == ano) & (df["Mês"] == mes)].copy()
        df_mes = df_mes.sort_values("Indice", ascending=True)
        df_mes["Liquido"]     = df_mes["Receitas"] - df_mes["Despesas"]
        df_mes["Saldo Final"] = df_mes["Saldo Inicial"] + df_mes["Liquido"]

        tot_rec = df_mes["Receitas"].sum()
        tot_des = df_mes["Despesas"].sum()
        tot_liq = tot_rec - tot_des
        tot_si  = df_mes["Saldo Inicial"].sum()
        tot_sf  = df_mes["Saldo Final"].sum()
        df_cx   = df_mes[df_mes["Caixa(Templo)"] > 0].sort_values("Caixa(Templo)", ascending=False)
        tot_cx  = df_cx["Caixa(Templo)"].iloc[0] if not df_cx.empty else 0.0

        liq_cls  = "pf-pill-lp" if tot_liq >= 0 else "pf-pill-ln"
        liq_seta = "&#9650;" if tot_liq >= 0 else "&#9660;"

        # Média por mês = acumulado da igreja até mes atual ÷ número do mês
        df_acum_pf = df[(df["Ano"] == ano) & (df["Mês"] <= mes)]

        linhas = []
        for _, row in df_mes.iterrows():
            cx = formatar_brl(row["Caixa(Templo)"]) if row["Caixa(Templo)"] > 0 else "—"
            df_ig_acum  = df_acum_pf[df_acum_pf["Igrejas"] == row["Igrejas"]]
            liq_ig_acum = df_ig_acum["Receitas"].sum() - df_ig_acum["Despesas"].sum()
            media_ig    = liq_ig_acum / mes if mes > 0 else 0.0
            linhas.append(
                '<tr>'
                '<td class="ch">' + str(row["Igrejas"])               + '</td>'
                '<td class="r">'  + formatar_brl(row["Receitas"])     + '</td>'
                '<td class="r">'  + formatar_brl(row["Despesas"])     + '</td>'
                '<td class="r">'  + badge(row["Liquido"])             + '</td>'
                '<td class="r">'  + badge(media_ig)                   + '</td>'
                '<td class="r">'  + formatar_brl(row["Saldo Inicial"])+ '</td>'
                '<td class="r">'  + formatar_brl(row["Saldo Final"])  + '</td>'
                '<td class="r">'  + cx                                + '</td>'
                '</tr>'
            )

        cx_total = formatar_brl(tot_cx) if tot_cx > 0 else "—"

        obs_rows = df_mes[
            df_mes["Observações"].notna() &
            (df_mes["Observações"].astype(str).str.strip() != "") &
            (df_mes["Observações"].astype(str).str.strip() != "—")
        ]
        if not obs_rows.empty:
            partes = [
                '<span style="font-weight:700;color:#5A1F05">' + str(r["Igrejas"]) + ':</span> ' + str(r["Observações"])
                for _, r in obs_rows.iterrows()
            ]
            obs_html = (
                '<div class="pf-obs">'
                '<span class="pf-obs-label">Obs.:</span>'
                + ' &nbsp;·&nbsp; '.join(partes) +
                '</div>'
            )
        else:
            obs_html = ""

        blocos += (
            '<div class="pf-month">'
              '<div class="pf-month-header">'
                '<h2>' + str(label) + '</h2>'
                '<div class="pf-pills">'
                  '<span class="pf-pill pf-pill-r">Rec: '  + formatar_brl(tot_rec) + '</span>'
                  '<span class="pf-pill pf-pill-d">Desp: ' + formatar_brl(tot_des) + '</span>'
                  '<span class="pf-pill ' + liq_cls + '">' + liq_seta + ' ' + formatar_brl(tot_liq) + '</span>'
                '</div>'
              '</div>'
              '<table class="pft">'
                '<thead><tr>'
                  '<th>Igreja</th>'
                  '<th class="r">Receitas</th>'
                  '<th class="r">Despesas</th>'
                  '<th class="r">Líquido</th>'
                  '<th class="r">Média/Ano</th>'
                  '<th class="r">Saldo Inicial</th>'
                  '<th class="r">Saldo Final</th>'
                  '<th class="r">Cai. Templo</th>'
                '</tr></thead>'
                '<tbody>' + "".join(linhas) + '</tbody>'
                '<tfoot><tr>'
                  '<td><strong>Total</strong></td>'
                  '<td class="r">' + formatar_brl(tot_rec)                                                           + '</td>'
                  '<td class="r">' + formatar_brl(tot_des)                                                           + '</td>'
                  '<td class="r">' + badge(tot_liq)                                                                  + '</td>'
                  '<td class="r">' + badge((df_acum_pf["Receitas"].sum() - df_acum_pf["Despesas"].sum()) / mes if mes > 0 else 0.0) + '</td>'
                  '<td class="r">' + formatar_brl(tot_si)                                                            + '</td>'
                  '<td class="r">' + formatar_brl(tot_sf)                                                            + '</td>'
                  '<td class="r">' + cx_total                                                                        + '</td>'
                '</tr></tfoot>'
              '</table>'
              + obs_html +
            '</div>'
        )

    rodape = '<div class="pf-footer">&#9642; IBF — Relatório Financeiro Mensal</div>'
    panfleto = cabecalho + blocos + rodape

    return (
        '<!DOCTYPE html><html lang="pt-BR"><head>'
        '<meta charset="UTF-8">'
        '<title>Relatório Financeiro IBF</title>'
        + CSS +
        '</head><body>'
        '<div class="panfleto-page">'
        '<div class="panfleto-col">' + panfleto + '</div>'
        '<div class="divisor"></div>'
        '<div class="panfleto-col">' + panfleto + '</div>'
        '</div>'
        '<script>window.onload=function(){window.print();}</script>'
        '</body></html>'
    )


# ─────────────────────────────────────────────
#  FUNÇÃO PÚBLICA — botão na sidebar
# ─────────────────────────────────────────────
def botao_download_relatorio(df_raw: pd.DataFrame) -> None:

    import streamlit as st

    periodos = (
        df_raw[["Ano", "Mês", "Data Referência"]]
        .drop_duplicates()
        .sort_values(["Ano", "Mês"], ascending=False)
        .head(3)
        .sort_values(["Ano", "Mês"], ascending=True)
        .values.tolist()
    )

    if not periodos:
        return

    html_bytes = build_panfleto(periodos, df_raw).encode("utf-8")
    nome       = f"relatorio_ibf_{datetime.now().strftime('%Y%m')}.html"

    st.markdown(
        """<hr style='border-color:rgba(255,255,255,0.15);margin:1.2rem 0 0.9rem'>
<div style='font-size:0.60rem;font-weight:700;text-transform:uppercase;
            letter-spacing:.12em;color:rgba(255,255,255,0.5);margin-bottom:8px;'>
    Relatório Impresso do Últimos 3 Meses
</div>""",
        unsafe_allow_html=True,
    )

    # Encode para data URI — abre direto no navegador ao clicar
    import base64 as _b64
    b64_html = _b64.b64encode(html_bytes).decode()
    data_uri = f"data:text/html;base64,{b64_html}"

    st.markdown(
        f"""<a href="{data_uri}" download="{nome}" target="_blank"
            style="
                display:flex;
                align-items:center;
                justify-content:center;
                gap:8px;
                width:100%;
                padding:9px 0;
                /*background:linear-gradient(135deg,#5A1F05,#BF5223);*/
                color:#fff;
                border-radius:8px;
                font-family:'Source Sans 3',sans-serif;
                font-size:0.78rem;
                font-weight:700;
                letter-spacing:.06em;
                text-decoration:none;
                border:1px solid rgba(255,255,255,0.15);
                box-shadow:0 2px 8px rgba(0,0,0,0.25);
                transition:opacity .15s;
                text-transform:uppercase;
            "
            onmouseover="this.style.opacity='.85'"
            onmouseout="this.style.opacity='1'">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
                 stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            Baixar Panfleto
        </a>""",
        unsafe_allow_html=True,
    )