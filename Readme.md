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


Web app:

1. minimalistik dizayn
2. real time manzillarni izlash
3. tour paketlarni band qilish

Telegram bot:

1. django bilan integratsiya(with db) 
2. turlarni band qidirish
3. Turlarni izlash