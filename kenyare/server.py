import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from kenyare.quotation.excel import make_excel
from kenyare.quotation.stack import get_quotation_input, upload_files
from kenyare.quotation.output import get_quotation_output

# Initialize Flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# Configure logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)

file_handler = RotatingFileHandler(
    os.path.join(log_dir, 'app.log'),
    maxBytes=10485760,  # 10MB
    backupCount=10
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# Console logging for development
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

static_dir = "static/outputs"
os.makedirs(static_dir, exist_ok=True)

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    app.logger.error(f"Bad request: {error}")
    return jsonify({"error": "Bad request", "message": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    app.logger.error(f"Not found: {error}")
    return jsonify({"error": "Not found", "message": str(error)}), 404

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(f"Server error: {error}")
    return jsonify({"error": "Internal server error", "message": "An unexpected error occurred"}), 500

# Health check endpoint
@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "version": os.getenv("APP_VERSION", "1.0.0")
    }), 200

@app.route('/outputs/<path:filename>')
def serve_static(filename):
    return send_from_directory('static/outputs', filename)

@app.route("/quotation/upload", methods=["POST"])
def quotation_upload():
    try:
        if not request.json:
            return jsonify({"error": "No JSON in request"}), 400

        proposal_path = request.json.get("proposal_path")
        audit_path = request.json.get("audit_path")
      
        if not proposal_path or not audit_path:
            return jsonify({"error": "Missing required fields"}), 400

        app.logger.info(f"Processing upload request for proposal: {proposal_path}")
        upload_files(proposal_path, audit_path)
        app.logger.info("Upload completed successfully")
        
        return jsonify({"data": {}, "message": "Files uploaded successfully"}), 200
    
    except Exception as e:
        app.logger.error(f"Error in upload: {str(e)}", exc_info=True)
        return jsonify({"error": "Upload failed", "message": str(e)}), 500

@app.route("/quotation/input", methods=["GET"])
def quotation_input():
    try:
        app.logger.info("Processing quotation input request")
        quotation_input = get_quotation_input()
        app.logger.info(f"Quotation input retrieved: {quotation_input}")
        
        return jsonify({
            "data": {"quotation_input": quotation_input},
            "message": "Quotation input retrieved successfully"
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error getting quotation input: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to get quotation input", "message": str(e)}), 500

@app.route("/quotation/output", methods=["POST"])
def quotation_output():
    try:
        if not request.json:
            return jsonify({"error": "No JSON in request"}), 400
        
        quotation_input = request.json.get("quotation_input")
        if not quotation_input:
            return jsonify({"error": "Missing quotation input"}), 400

        app.logger.info("Processing quotation output request")
        quotation_output = get_quotation_output(quotation_input)
        
        excel_download_url = "/outputs/quotation.xlsx"
        excel_path = f"static{excel_download_url}"
        
        make_excel(
            quotation_input["reinsured_name"],
            quotation_input["broker_name"],
            quotation_input["insured_name"],
            quotation_output,
            excel_path,
        )
        
        quotation_output["excel_download_url"] = excel_download_url
        app.logger.info(f"Quotation output generated: {quotation_output}")
        
        return jsonify({
            "data": {"quotation_output": quotation_output},
            "message": "Quotation output generated successfully"
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error generating quotation output: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to generate quotation output", "message": str(e)}), 500

if __name__ == "__main__":
    # Get configuration from environment variables
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV") == "development"
    
    app.logger.info(f"Starting server on port {port}")
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )
