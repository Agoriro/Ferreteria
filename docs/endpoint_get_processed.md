# Endpoint: Obtener Sugeridos con Status Processed

## Descripción
Este endpoint retorna todos los registros de la tabla `sugerido_compras` que tienen el estado **Processed**.

---

## Información del Endpoint

| Campo | Valor |
|-------|-------|
| **URL** | `/api/v1/sugerido-compras/processed` |
| **Método** | `GET` |
| **Autenticación** | Bearer Token (JWT) |

---

## Request

### Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

### Parámetros
Este endpoint no requiere parámetros.

---

## Response

### Código 200 - Éxito

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "empresa": "IMPERIO",
      "proveedor": "PROVEEDOR EJEMPLO S.A.S",
      "cod_prod": "ABC123",
      "descripcion": "Tornillo galvanizado 1/4 x 2",
      "unidad_medida": "UND",
      "cantidad_proveedor": 100.00,
      "valor_unitario_proveedor": 2500.50
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "empresa": "IMPERIO",
      "proveedor": "FERRETERÍA XYZ",
      "cod_prod": "DEF456",
      "descripcion": "Clavo 2 pulgadas",
      "unidad_medida": "KG",
      "cantidad_proveedor": 50.00,
      "valor_unitario_proveedor": 8500.00
    }
  ],
  "total": 2
}
```

### Campos de respuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID | Identificador único del registro |
| `empresa` | string | Nombre de la empresa |
| `proveedor` | string \| null | Nombre del proveedor |
| `cod_prod` | string | Código del producto |
| `descripcion` | string \| null | Descripción del producto |
| `unidad_medida` | string \| null | Unidad de medida del producto |
| `cantidad_proveedor` | number \| null | Cantidad confirmada por el proveedor |
| `valor_unitario_proveedor` | number \| null | Precio unitario del proveedor |
| `total` | number | Total de registros retornados |

---

## Ejemplo de Consumo (JavaScript/Fetch)

```javascript
const getProcessedSugeridos = async () => {
  const response = await fetch('/api/v1/sugerido-compras/processed', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  if (!response.ok) {
    throw new Error('Error al obtener registros procesados');
  }
  
  const data = await response.json();
  return data; // { items: [...], total: number }
};
```

---

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| 401 | No autorizado - Token inválido o expirado |
| 500 | Error interno del servidor |

---

## Notas
- Este endpoint solo retorna registros con `status = 'Processed'`
- Los registros llegan a este estado después de ser procesados por el proveedor mediante el endpoint `/bulk-update-proveedor`
- Los campos `cantidad_proveedor` y `valor_unitario_proveedor` contienen los valores ingresados por el proveedor
