---
# 📡 Portfolio API Server

This repository contains the **Portfolio API**, a backend service built with **FastAPI** to support:

- 📊 SQL-based data querying
- 🔐 Password generation
- 📥 Multimedia downloading and processing (YouTube, Vimeo, TikTok, and more)

---

## 🚀 Deployment

This API is hosted on **Render.com** and available at:

# Deployment
![deployments](https://raw.githubusercontent.com/JorgeCardona/portfolio-api-server/refs/heads/main/images/deployments.png)

# Python Deployment
![python](https://raw.githubusercontent.com/JorgeCardona/portfolio-api-server/refs/heads/main/images/despliegue_python.jpg)

# Docker Deployment
![docker](https://raw.githubusercontent.com/JorgeCardona/portfolio-api-server/refs/heads/main/images/despliegue_docker.jpg)

- 🌐 **Production URL**: [https://portfolio-api-server-7uvi.onrender.com/](https://portfolio-api-server-7uvi.onrender.com/)
- 🔧 **Deployment Management**: [https://dashboard.render.com](https://dashboard.render.com) (SSO login)

It is connected to the GitHub repository:

- 📁 [JorgeCardona/portfolio-api-server](https://github.com/JorgeCardona/portfolio-api-server)

---

## ⚙️ Local Development

To run locally:

```bash
uvicorn application.main:app --reload
````

> Ensure you have Python 3.10+ and run `pip install -r requirements.txt`

---

## 🧩 Project Structure

```
application/
├── main.py                          # FastAPI entrypoint
├── services/                        # Application logic (use cases)
├── domain/entities/models/         # Pydantic schemas
├── configuration/                  # DB path, CORS, environment config
└── ...
```

---

## 📖 API Endpoints

### 🔧 `GET /tables`

Returns available SQL tables and their columns.

**Response:**

```json
{
  "users": [
    {"id": "int"},
    {"email": "str"}
  ]
}
```

---

| Table Name      | Columns                                                                                                   |
|----------------|------------------------------------------------------------------------------------------------------------|
| albums          | AlbumId, Title, ArtistId                                                                                  |
| sqlite_sequence | name, seq                                                                                                  |
| artists         | ArtistId, Name                                                                                            |
| customers       | CustomerId, FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId |
| employees       | EmployeeId, LastName, FirstName, Title, ReportsTo, BirthDate, HireDate, Address, City, State, Country, PostalCode, Phone, Fax, Email |
| genres          | GenreId, Name                                                                                             |
| invoices        | InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total |
| invoice_items   | InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity                                                    |
| media_types     | MediaTypeId, Name                                                                                         |
| playlists       | PlaylistId, Name                                                                                          |
| playlist_track  | PlaylistId, TrackId                                                                                       |
| tracks          | TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice                    |
| sqlite_stat1    | tbl, idx, stat                                                                                            |

### 🧮 `POST /query`

Executes raw SQL queries.

**Request:**

```json
{
  "query": "SELECT * FROM artists LIMIT 10"
}
```

**Response:** JSON array of rows.

---

### 🔐 `POST /generate-password`

Generates a secure password.

**Request:**

```json
{
  "length": 16,
  "uppercase": true,
  "lowercase": true,
  "numbers": true,
  "symbols": true
}
```

**Response:**

```json
{
  "password": "A9d!kSl38vD#l2Wp"
}
```

---

## 🎬 Multimedia Download API

Supports downloading and converting videos from platforms like YouTube, TikTok, Vimeo, etc.

---

### ⚡ `GET /get-multimedia-file`

Creates and returns a `.zip` with the downloaded and processed video/audio.
Automatically deletes the file after 30 minutes.

**Query Parameters:**

* `url` (required): Link to video (e.g. YouTube)
* `format` (required): `"mp3"`, `"mp4"`, or `"original"`
* `trim_start` (optional): `"HH:MM:SS"`
* `trim_end` (optional): `"HH:MM:SS"`
* `include_thumbnail` (default: true)
* `subtitle_langs` (default: `["en", "es"]`)

**Example:**

```
GET /get-multimedia-file?url=https://youtu.be/abc123&format=mp3&trim_start=00:00:10&trim_end=00:00:30
```

---

### 🛠 `POST /create-multimedia-file`

Generates the media zip file but does not serve it directly.

**Request:**

```json
{
  "url": "https://youtu.be/abc123",
  "format": "mp4",
  "trim_start": "00:00:05",
  "trim_end": "00:00:20",
  "include_thumbnail": true,
  "subtitle_langs": ["en"]
}
```

**Response:**

```json
{
  "filename": "MyVideo.zip"
}
```

---

### 📥 `GET /download-multimedia-file`

Downloads a zip file previously created via `/create-multimedia-file`.

**Query:**

```
?filename=MyVideo.zip
```

---

### 🗑️ `DELETE /delete-multimedia-file`

Manually deletes a `.zip` file from the server.

**Query:**

```
?filename=MyVideo.zip
```

**Response:**

```json
{
  "detail": "MyVideo.zip deleted successfully."
}
```

---

## ✅ Notes

* `.zip` files are automatically deleted 30 minutes after creation via `get-multimedia-file`.
* Frontend clients can use `/create-multimedia-file` to build the file and later download it using `/download-multimedia-file`, with an optional manual delete.

---

## 📂 License

This project is open source and available under the [MIT License](LICENSE).

```