Run with local:

```python
pip install -r requirements.txt

make mg (for migrations)

make run ( run app )
```
Run with docker:

```
# Development
docker-compose up --build

# Production
docker build -t myproject .
docker run -p 8000:8000 myproject

```