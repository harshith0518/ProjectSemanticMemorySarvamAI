import { createRoot } from "react-dom/client";
import { setNonce } from "get-nonce";
import "@fontsource-variable/dm-sans";
import "@fontsource-variable/fraunces";
import "./styles.css";
import App from "./App";

const nonce = document.querySelector<HTMLMetaElement>(
  'meta[name="kivi-style-nonce"]',
)?.content;
if (nonce && nonce !== "__KIVI_STYLE_NONCE__") setNonce(nonce);
createRoot(document.getElementById("root")!).render(<App />);
