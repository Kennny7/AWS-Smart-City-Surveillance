# docker/Dockerfile

# =======================
# 1. BASE IMAGE
# =======================
FROM python:3.9-slim

# =======================
# 2. INSTALL SYSTEM DEPENDENCIES
# =======================
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# =======================
# 3. SET WORKDIR
# =======================
WORKDIR /app

# Add the project root to PYTHONPATH
ENV PYTHONPATH=/app

# =======================
# 4. COPY REQUIREMENTS
# =======================
COPY requirements.txt .

# =======================
# 5. INSTALL DEPENDENCIES
# =======================
RUN pip install --no-cache-dir -r requirements.txt

# =======================
# 6. COPY PROJECT FILES
# =======================
COPY . .

# =======================
# 7. EXPOSE PORT
# =======================
EXPOSE 5000

# =======================
# 8. COPY ENTRYPOINT & MAKE EXECUTABLE
# =======================
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# =======================
# 9. DEFAULT COMMAND
# =======================
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "src/web_dashboard/app.py"]
