# Information about project

| Website Language | Program Language | Framework | Database      | Build     |
| ---------------- | ---------------- | --------- | ------------- | --------- |
| Vietnamese       | Python 3.12      | Django 5  | Postgresql 17 | Docker 27 |

<br>
<br>

# Build with Docker (recommend)
### Download and install tools
> #### Docker
> - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
> - If you use `MacOS` you can use [Orbstack](https://orbstack.dev/) for fast and light

<br>

### Prepair for project
> #### Create .env file
> - Copy file `.env.example` to `.env` in `docker` folder
> - Config env variable for project

<br>

### Some docker command
#### In the first change directory to `docker` folder

> #### Build and up docker
> ```bash
> docker-compose up --build -d
> ```


> #### Shutdown project
> ```bash
> cd docker && docker-compose down && cd ..
> ```

<br>
<br>

# Build without Docker
### Download and install tools
> #### Python3
> - [Official website](https://www.python.org/)
> - [Microsoft store version 3.13](https://apps.microsoft.com/detail/9PNRBTZXMB4Z?hl=en-us&gl=VN&ocid=pdpshare)

> #### PostgreSQL
> - [Official website](https://www.postgresql.org/)

<br>

### Prepair for project
> #### Create .env file
> - Copy file `.env.example` from `docker` folder to `.env` in `root` folder
> - Config env variable for project

> #### Create Python virtual environment
> ```bash
> python -m venv .venv
> ```

> #### Active Python virtual environment
> - With Windows OS
>   ```bash
>   .\.venv\Scripts\activate
>   ```
>   Note: If can not active you can try: Open `Powershell` with `Adminstrator role` and run this command
>   ```bash
>   Set-ExecutionPolicy Unrestricted -Force
>   ```
> - With Linux/ MacOS
>   ```bash
>   source .venv/bin/activate
>   ```

> #### Install Python packages from requirements
> ```bash
> pip install -r requirements.txt
> ```

<br>

### Run Django server
> - Change directory to `src` folder
> - Run server
>   ```
>   python manage.py runserver 0.0.0.0:80
>   ```
>   Note:
>   - `0.0.0.0` is public server to local network, if you don't want to public you can use `127.0.0.1`
>   - `80` is port of server. Default HTTP port `80`, and HTTPS is `443`

<br>
<br>

# Some Django command
>#### Create app
>```bash
> python manage.py startapp [app_name]
>```

>#### Make migrations
>```bash
> python manage.py makemigrations
>```

>#### Run migrate
>```bash
> python manage.py migrate
>```

<br>
<br>

# Thank you so much
