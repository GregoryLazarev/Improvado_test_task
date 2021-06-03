В данном репозитории представлен вариант решения задания для потенциальных кандидатов на позицию Junior-девелоперов.

# Требования для запуска

При запуске скрипта необходимо указать имена входных файлов, используя аргумент `-f` или `--file`. 
Например, для того, чтобы скрипт обработал файлы *csv_data_1.csv*, *csv_data_2.csv*, *json_data.json*, *xml_data.xml*, необходимо выполнить следующую команду:

```
python script.py -f csv_data_1.csv csv_data_2.csv json_data.json xml_data.xml
```

# Требования к входным данным

Программа работает с файлами следующих форматов:
* `.csv`
* `.json`
* `xml`.

## Требования к `.csv` файлам

* В качестве разделителя в файле должна использоваться запятая (',')
* `.csv` файл может иметь одну из следующих структур:

    Первый вариант структуры `.csv`

    | D1  | D2  | ... | Dn  | M1  | M2  | ... | Mn  |
    | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
    |  s  |  s  | ... |  s  |  i  |  i  | ... |  i  |
    | ... | ... | ... | ... | ... | ... | ... | ... |

    Второй вариант структуры `.csv`

    | D1  | D2  | ... | Dn  | M1  | M2  | ... | Mn  | ... | Mz  |
    | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
    |  s  |  s  | ... |  s  |  i  |  i  | ... |  i  | ... |  i  |
    | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

    Где _z_ > _n_, _p_ >= _n_, _s_ строка и _i_ целое число.

## Требования к `.json` файлам

`.json` файл должен иметь следуующую структуру:

```
{
  "fields": [
    {
      "D1": "s",
      "D2": "s",
      ...
      "Dn": "s",
      "M1": i,
      ...
      "Mp": i,
    },
    ...
  ]
}
```
Где _p_ >= _n_, _s_ строка и _i_ целое число.

## Требования к `.xml` файлам

`.xml` файл должен содержать в себе следующую структуру:

```
<objects>
  <object name="D1">
    <value>s</value>
  </object>
  <object name="D2">
    <value>s</value>
  </object>
  ...
  <object name="Dn">
    <value>s</value>
  </object>
  <object name="M1">
    <value>i</value>
  </object>
  <object name="M2">
    <value>i</value>
  </object>
  ...
  <object name="Mn">
    <value>i</value>
  </object>
</objects>
```
Где _s_ строка и _i_ целое число.

# Выходные данные

## Basic
Выходной файл представляет собой `.tsv` файл со следующей структурой:

| D1  | D2  | ... | Dn  | M1  | M2  | ... | Mn  |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|  s  |  s  | ... |  s  |  i  |  i  | ... |  i  |
| ... | ... | ... | ... | ... | ... | ... | ... |

Он отсортирован по колонке **D1** и содержать даннные из всех входных файлов.

В качестве разделителя столбцов использован символ табуляции `\t`

## Advanced
Выходной файл представляет собой `.tsv` файл со следующей структурой:
| D1  | D2  | ... | Dn  | MS1 | MS2 | ... | MSn |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|  s  |  s  | ... |  s  |  i  |  i  | ... |  i  |
| ... | ... | ... | ... | ... | ... | ... | ... |

В колонках **MS1**...**MSn** находится суммы знаений соответствующих **M1**...**Mn** из входных файлов, сгруппированные
по уникальнным значениям комбинаций строк из **D1**...**Dn**.

В качестве разделителя столбцов использован символ табуляции `\t

# Вывод ошибок
## Некорректные входные данные
Если один или несколько входных файлов имеют некорректный формат или не существуют, то информация об этом будет выведена в консоль, а выполнение программы прекратится с кодом ошибки 1.

Если файл с указанным именем не существует, то будет выведено сообщение следующего вида:
```
File <имя_файла> not found.
```

Если файл существует, но имеет некорректный формат, то будет выведено сообщение следующего вида:
```
Invalid format of <имя_файла>
```

## Ошибка в значении столбца мер (measures) Mn
Если одно из значений мер (measures) Mn в строке будет не целочисленное, то эта строка не будет учтена в итоговом файле, а в конце работы программы в консоль будет выведена информация об ошибке, содержащая имя файла, номер строки и название столбца, содержащего некорректное значение.

Пример ошибки, если некорректное значение находится в столбце *M2* первой строки файла *csv_data_1.csv*:
```
Ошибка!
Файл: csv_data_1.csv
Строка: 1
Столбец: M2
Невозможно преобразовать данное значение в целочисленное
```