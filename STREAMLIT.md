# Use the graphical interface

Place `app.py` in your existing ParticleID-AI project folder, alongside `pyproject.toml`. Keep your own trained file at `runs/demo/model.joblib`. The app resolves this path relative to itself, so it does not depend on the terminal's current directory.

From your project folder in Windows PowerShell:

```powershell
.\.venv\Scripts\python -m pip install streamlit
.\.venv\Scripts\python -m streamlit run app.py
```

Open the local URL printed in your terminal (usually http://localhost:8501). The form starts with **5.0 GeV/c**, **33.36 ns**, and **12 photoelectrons**. Click **Predict particle** to run the saved classifier's `predict` and `predict_proba` methods. Edit the values and click again for another prediction. Press Ctrl+C in the terminal to stop the server.

There is no hardcoded prediction, replacement model, retraining, or network inference service. The app requires the original ParticleID-AI dictionary bundle containing `model`, `features` and `species`. Missing files and incompatible formats produce a visible error rather than a demo output. Only load trusted joblib files. Retain the training environment's scikit-learn version when loading its model.

For a new install using this updated project, `python -m pip install -e ".[ui]"` also installs Streamlit. The model itself is not included in the UI update ZIP; keep your existing model.

The interface uses [Streamlit forms](https://docs.streamlit.io/develop/concepts/architecture/forms) to submit the three measurements together and [resource caching](https://docs.streamlit.io/develop/concepts/architecture/caching) to avoid reloading an unchanged model.
