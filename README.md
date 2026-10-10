# Local Multi-Page RAG Agent

An intelligent Python application utilizing local LLMs via **Ollama**, a local vector database through **ChromaDB**, and **Pydantic** structured outputs to perform Retrieval-Augmented Generation (RAG) on multi-page documents and images.

## How It Works
The application orchestrates a modular data processing pipeline across five distinct steps:
1. **Ingestion:** The system routes raw data inputs based on your workflow choice—streaming real-time camera frames via OpenCV, parsing standalone image formats, or cleanly decomposing multi-page PDFs into distinct temporary image frames within the `src/` folder.
2. **Vision Extraction (OCR):** The system sequentially channels image matrices through `easyocr` to strip out raw character layers. The text fragments are grouped, tagged by page indices, and partitioned into unified semantic text blocks.
3. **Embedding Generation:** Text blocks are forwarded to the local `ollama` embedding API, transforming text strings into high-dimensional data vector profiles using the `llama3.2:1b` architecture.
4. **Vector Memory Storage:** The generated vectors and source texts are indexed into a local `chromadb` layer. To guarantee data fresh sessions, the underlying collection is wiped completely clean on every runtime execution loop.
5. **Retrieval & Inference:** When a text query is entered, the system calculates query embedding distances to grab the top 3 most relevant textual context matches from database records. These reference blocks are structured directly into a template file (`src/prompt.txt`) and evaluated by the LLM. The final output is cleanly packaged and returned via rigid Pydantic object model structures.

## Features
- **Document Ingestion:** Supports capturing document images live via a webcam stream, processing local image assets, or extracting and slicing text layers across multi-page PDFs.
- **Local Embedding & Vector Storage:** Transforms raw unstructured text into high-dimensional data vector streams entirely locally using `llama3.2:1b`, indexing them securely into a persistent `chromadb` layer.
- **Structured Data Inference:** Validates model answers against strict Pydantic configurations to guarantee uniform object schemas without runtime string formatting errors.

## Technologies Used
- **Language:** Python 3.x
- **Local AI Orchestration:** `ollama` (Running `llama3.2:1b`)
- **Vector Base Engine:** `chromadb`
- **Data Slicing & Vision:** `pandas`, `pydantic`, `easyocr`, `opencv`, and `pdf2image`.

## Prerequisites
- Python 3.8 or higher.
- [Ollama](https://ollama.com) installed on your machine.
- The local Llama model pulled via terminal:
  ```bash
  ollama pull llama3.2:1b
  ```

## Installation & Run
1. Clone the repository:
   ```bash
   git clone https://github.com/infiniteloop22/local-multipage-rag-agent
   cd local-multipage-rag-agent
   ```
2. Activate your virtual environment (`venv`) through your terminal:
   - **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
   - **macOS / Linux:** `source .venv/bin/activate`
3. Install the required data processing libraries using the requirements file:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the pipeline from your project root folder:
   ```bash
   python src/main.py
   ```

## Usage
1. Launch the script in your terminal using the root entry execution command `python src/main.py`.
2. Choose an entry interface by entering your choice numeric token:
   - `1`: Triggers your webcam stream, captures an asset frame on `[SPACEBAR]`, runs adaptive thresholding, and loads your vector base.
   - `2`: Prompts you for a file path, flattens PDF layouts into temporary image assets, stores semantic text blocks, and launches an interactive chat session for continuous text processing queries.
   - `3`: Launches an empty context workspace conversation layout to query the local model engine directly.
3. Type `exit` to terminate active terminal sessions. Temporary page assets stored inside `src/` are cleared dynamically.