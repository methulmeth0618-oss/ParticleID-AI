"""Run with: python -m streamlit run app.py

Loads only the local model at runs/demo/model.joblib. No retraining or fallback.
"""
from pathlib import Path
import hashlib
import joblib
import numpy as np
import streamlit as st

MODEL_PATH = Path(__file__).resolve().parent / "runs" / "demo" / "model.joblib"
FEATURES = ["momentum_GeV_c", "tof_ns", "cherenkov_photoelectrons"]


@st.cache_resource(show_spinner="Loading your trained model…")
def load_model(path, modified_ns, size):
    # File metadata keys invalidate the cache when the saved model changes.
    # joblib files execute Python when loaded; use only your trusted local model.
    artifact = joblib.load(path)
    if not isinstance(artifact, dict) or artifact.get("features") != FEATURES:
        raise ValueError("Expected a ParticleID-AI model bundle with the three detector features in training order.")
    model = artifact.get("model")
    species = artifact.get("species")
    if not hasattr(model, "predict") or not hasattr(model, "predict_proba"):
        raise ValueError("The saved bundle does not contain a fitted classifier.")
    if not isinstance(species, (list, tuple)) or not species:
        raise ValueError("The model bundle is missing species labels.")
    if getattr(model, "n_features_in_", None) != 3:
        raise ValueError("The trained classifier expects a different number of features.")
    for label in model.classes_:
        if not isinstance(label, (int, np.integer)) or not 0 <= label < len(species):
            raise ValueError("Classifier classes do not match the saved species mapping.")
    return artifact, hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    st.set_page_config(page_title="ParticleID-AI", page_icon="⚛️", layout="centered")
    st.title("ParticleID-AI")
    st.write("Enter detector measurements to classify one event with your trained model.")
    try:
        info = MODEL_PATH.stat()
        artifact, fingerprint = load_model(str(MODEL_PATH), info.st_mtime_ns, info.st_size)
    except FileNotFoundError:
        st.error("Model not found. Place your trained model at runs/demo/model.joblib beside this app's folder.")
        st.code(str(MODEL_PATH))
        st.info("If you have not trained it yet, run: particleid run --output runs/demo")
        st.stop()
    except Exception as error:
        st.error(f"Could not load the saved model: {error}")
        st.info("Use the original training environment and its package versions. No substitute model was loaded.")
        st.stop()

    st.caption("Loaded: runs/demo/model.joblib · " + type(artifact['model']).__name__)
    with st.form("event"):
        momentum = st.number_input("Momentum (GeV/c)", min_value=0.000001, value=5.0, step=0.1, format="%.6f")
        tof = st.number_input("Time of flight (ns)", min_value=0.000001, value=33.36, step=0.01, format="%.6f")
        npe = st.number_input("Cherenkov photoelectron count", min_value=0, value=12, step=1)
        submitted = st.form_submit_button("Predict particle", type="primary")

    if submitted:
        X = np.array([[momentum, tof, npe]], dtype=float)
        if not np.isfinite(X).all() or momentum <= 0 or tof <= 0 or npe < 0 or int(npe) != npe:
            st.error("Enter finite positive momentum and TOF, and a nonnegative integer photoelectron count.")
            st.stop()
        try:
            model = artifact['model']
            predicted_class = model.predict(X)[0]
            scores = np.asarray(model.predict_proba(X)[0], dtype=float)
            if scores.shape != (len(model.classes_),) or not np.isfinite(scores).all():
                raise ValueError("The model returned invalid class scores.")
            label = artifact['species'][int(predicted_class)]
            st.success(f"Predicted particle: {label}")
            st.caption(f"Submitted event: {momentum:g} GeV/c · {tof:g} ns · {npe} photoelectrons")
            st.subheader("Model scores")
            for class_id, score in zip(model.classes_, scores):
                st.write(f"**{artifact['species'][int(class_id)]}** — {score:.2%}")
                st.progress(float(np.clip(score, 0, 1)))
            st.caption("Scores come directly from predict_proba; they are not calibrated certainty estimates.")
            config = artifact.get('config', {})
            if 'p_min' in config and 'p_max' in config and not config['p_min'] <= momentum <= config['p_max']:
                st.warning(f"Momentum is outside the training range ({config['p_min']}–{config['p_max']} GeV/c).")
        except Exception as error:
            st.error(f"Prediction failed: {error}")

    st.divider()
    st.caption("This is a real prediction from your saved ML model. Its training data are synthetic; experimental performance has not been validated.")
    with st.expander("Model details"):
        st.code(str(MODEL_PATH))
        st.write("Feature order:", FEATURES)
        st.write("Training configuration:", artifact.get('config', {}))
        st.write("Training package versions:", artifact.get('environment', {}))
        st.caption("SHA-256: " + fingerprint)


if __name__ == "__main__":
    main()
