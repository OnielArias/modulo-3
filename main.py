from pymongo import MongoClient

# Conexión a la base de datos MongoDB
cliente = MongoClient('localhost', 27017)
base_datos = cliente['nombre de la base de datos']

# Colección para almacenar las palabras del diccionario
coleccion_palabras = base_datos['palabras']

while True:
    print('Seleccione una opción:')
    print('1) Agregar nueva palabra')
    print('2) Editar palabra existente')
    print('3) Eliminar palabra existente')
    print('4) Ver listado de palabras')
    print('5) Buscar significado de palabra')
    print('6) Salir')

    opcion = input('> ')

    try:
        opcion = int(opcion)

        if opcion == 1:
            palabra = input('Ingrese la palabra: ')
            significado = input('Ingrese el significado: ')

            nueva_palabra = {'palabra': palabra, 'significado': significado}
            id_palabra = coleccion_palabras.insert_one(nueva_palabra).inserted_id

            print(f'La palabra ha sido agregada exitosamente con ID {id_palabra}.')

        elif opcion == 2:
            id_palabra_editar = input('Ingrese el ID de la palabra a editar: ')
            palabra_nueva = input('Ingrese la nueva palabra: ')
            significado_nuevo = input('Ingrese el nuevo significado: ')

            palabra_editar = coleccion_palabras.find_one({'_id': id_palabra_editar})
            palabra_editar['palabra'] = palabra_nueva
            palabra_editar['significado'] = significado_nuevo
            coleccion_palabras.update_one({'_id': id_palabra_editar}, {'$set': palabra_editar})

            print('La palabra ha sido editada exitosamente.')

        elif opcion == 3:
            id_palabra_eliminar = input('Ingrese el ID de la palabra a eliminar: ')
            coleccion_palabras.delete_one({'_id': id_palabra_eliminar})

            print('La palabra ha sido eliminada exitosamente.')

        elif opcion == 4:
            lista_palabras = coleccion_palabras.find()

            print('Listado de palabras:')
            for palabra in lista_palabras:
                print(f'{palabra["_id"]} - {palabra["palabra"]}: {palabra["significado"]}')

        elif opcion == 5:
            palabra_buscar = input('Ingrese la palabra a buscar: ')

            lista_palabras = coleccion_palabras.find({'palabra': {'$regex': palabra_buscar, '$options': 'i'}})

            if lista_palabras.count() > 0:
                print('Resultados de la búsqueda:')
                for palabra in lista_palabras:
                    print(f'{palabra["palabra"]}: {palabra["significado"]}')
            else:
                print('No se encontraron resultados para la búsqueda.')

        elif opcion == 6:
            print('Hasta luego.')
            break

        else:
            print('Opción inválida. Por favor, seleccione una opción válida.')

    except ValueError:
        print('Opción inválida. Por favor, seleccione una opción válida.')