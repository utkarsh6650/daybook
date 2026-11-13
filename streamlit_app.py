from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Daybook",
    page_icon="📓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Remove Streamlit default chrome and padding so the HTML app fills the viewport
st.markdown(
    """
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .stAppDeployButton {display: none;}
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            display: block;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Locate Daybook.html (supports both 'Daybook.html' and 'daybook.html')
base_dir = Path(__file__).parent
html_path = base_dir / "Daybook.html"
if not html_path.exists():
    html_path = base_dir / "daybook.html"

if html_path.exists():
    html_content = html_path.read_text(encoding="utf-8")

    # Polyfill the export button download helper so JSON/Markdown backups work in standard browsers
    download_polyfill = """
    <script>
    window.claude = window.claude || {
      use: function(mod) {
        if (mod === 'downloads') {
          return Promise.resolve({
            save: function(opts) {
              return new Promise(function(resolve) {
                var blob = new Blob([opts.data], {type: 'text/plain;charset=utf-8'});
                var url = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = opts.filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                resolve();
              });
            }
          });
        }
        return Promise.resolve(null);
      }
    };
    </script>
    """
    html_content = html_content.replace("<body>", "<body>" + download_polyfill, 1)

    components.html(html_content, height=900, scrolling=True)
else:
    st.error("Could not find `Daybook.html` in the repository root.")