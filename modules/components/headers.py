"""
Composants pour les headers et titres de vues.
"""

import streamlit as st


def render_view_header(icon_svg: str, title: str, subtitle: str = "") -> None:
    """
    Affiche un header de vue avec icône, titre et sous-titre optionnel.
    
    Args:
        icon_svg: Code SVG de l'icône
        title: Titre principal
        subtitle: Sous-titre optionnel
    """
    subtitle_html = (
        f"""<span style="
                font-size: 0.7rem;
                color: #64748b;
                font-weight: 400;
                display: block;
                margin-top: 0.08rem;
            ">{subtitle}</span>"""
        if subtitle
        else ""
    )
    st.markdown(
        f"""
        <div style="
            margin: -0.5rem 0 0.4rem;
            background: linear-gradient(to right, #ffffff 0%, #fcfcfc 100%);
            border: 1px solid #e2e8f0;
            border-left: 3px solid #D92332;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
            padding: 0.4rem 0.7rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-radius: 6px;
        ">
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                width: 24px;
                height: 24px;
                background: rgba(217, 35, 50, 0.06);
                border-radius: 5px;
            ">
                {icon_svg}
            </div>
            <div>
                <span style="
                    font-weight: 600;
                    color: #1e293b;
                    font-size: 0.9rem;
                    letter-spacing: -0.01em;
                ">
                    {title}
                </span>
                {subtitle_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
