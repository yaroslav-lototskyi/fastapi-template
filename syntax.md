## 1. Змінні та типи

| Дія | Python | TypeScript |
|-----|--------|------------|
| Оголошення змінних | ```python
x = 10
name = "Bob"
pi = 3.14
``` | ```ts
let x: number = 10;
let name: string = "Bob";
let pi: number = 3.14;
``` |
| Динамічні типи | ✅ автоматично | ❌ треба вказувати тип |
| Константа | ```python
PI = 3.14  # просто угода, const немає
``` | ```ts
const PI: number = 3.14;
``` |
| Перевірити тип | ```python
print(type(x))
``` | ```ts
console.log(typeof x);
``` |