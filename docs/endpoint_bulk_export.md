# Endpoint: Bulk Export con Generación de Órdenes de Compra

## Descripción
Este endpoint actualiza múltiples registros de `sugerido_compras` al estado **Exported** y genera objetos JSON con la estructura de órdenes de compra (OC). Cada combinación de empresa + proveedor genera una orden independiente.

---

## Información del Endpoint

| Campo | Valor |
|-------|-------|
| **URL** | `/api/v1/sugerido-compras/bulk-export` |
| **Método** | `PATCH` |
| **Autenticación** | Bearer Token (JWT) |

---

## Request

### Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

### Body
```json
{
  "ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "550e8400-e29b-41d4-a716-446655440001",
    "550e8400-e29b-41d4-a716-446655440002"
  ]
}
```

---

## Response

### Código 200 - Éxito

```json
{
  "message": "Registros actualizados a 'Exported' correctamente",
  "updated_count": 3,
  "updated_ids": ["id1", "id2", "id3"],
  "ordenes_compra": [
    {
      "encabezado": {
        "empresa": "IMPERIO",
        "tipo_documento": "OC",
        "prefijo": "CO",
        "documento_numero": "1234",
        "fecha": "08/02/2026",
        "tercero_interno": "39425084",
        "tercero_externo": "900123456",
        "prefijo_dto_ext": "",
        "numero_dto_ext": 0,
        "nota": "Orden de compra generada desde la Herramienta Web",
        "forma_pago": "CREDITO",
        "verificado": -1,
        "anulado": 0,
        "fecha_emision": "",
        "personalizado_1": "",
        "personalizado_2": "",
        "personalizado_3": "",
        "personalizado_4": "",
        "personalizado_5": "",
        "personalizado_6": "",
        "personalizado_7": "",
        "personalizado_8": "",
        "personalizado_9": "",
        "personalizado_10": "",
        "personalizado_11": "",
        "personalizado_12": "",
        "personalizado_13": "",
        "personalizado_14": "",
        "personalizado_15": "",
        "importacion": "",
        "sucursal": "",
        "clasificacion": ""
      },
      "detalles": [
        {
          "producto": "ABC123",
          "bodega": "Principal",
          "unidad_de_medida": "UND",
          "cantidad": 100,
          "iva": 19.00,
          "valor_unitario": 2500.50,
          "descuento": 0,
          "vencimiento": "08/02/2026",
          "nota": "",
          "centro_costos": "",
          "codigo_centro_costos": "",
          "personalizado_1": "",
          "personalizado_2": "",
          "personalizado_3": "",
          "personalizado_4": "",
          "personalizado_5": "",
          "personalizado_6": "",
          "personalizado_7": "",
          "personalizado_8": "",
          "personalizado_9": "",
          "personalizado_10": "",
          "personalizado_11": "",
          "personalizado_12": "",
          "personalizado_13": "",
          "personalizado_14": "",
          "personalizado_15": ""
        }
      ]
    }
  ]
}
```

---

## Estructura de Respuesta

### campos principales

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `message` | string | Mensaje de confirmación |
| `updated_count` | number | Cantidad de registros actualizados |
| `updated_ids` | string[] | Lista de IDs actualizados |
| `ordenes_compra` | OrdenCompra[] | Lista de órdenes de compra generadas |

### Encabezado (OrdenCompra.encabezado)

| Campo | Valor |
|-------|-------|
| `tipo_documento` | Siempre "OC" |
| `prefijo` | Siempre "CO" |
| `documento_numero` | MAX(Numero_Documento) + N (incremental) |
| `fecha` | Fecha actual (DD/MM/YYYY) |
| `tercero_interno` | Siempre "39425084" |
| `tercero_externo` | identificacion_tercero del proveedor |
| `nota` | "Orden de compra generada desde la Herramienta Web" |
| `forma_pago` | Siempre "CREDITO" |
| `verificado` | Siempre -1 |
| `anulado` | Siempre 0 |

### Detalle (OrdenCompra.detalles[])

| Campo | Origen |
|-------|--------|
| `producto` | sugerido_compras.cod_prod |
| `bodega` | Siempre "Principal" |
| `unidad_de_medida` | sugerido_compras.unidad_medida |
| `cantidad` | sugerido_compras.cantidad_proveedor |
| `iva` | Vista_Tabla_Inventarios.Iva (2 decimales) |
| `valor_unitario` | sugerido_compras.valor_unitario_proveedor |
| `descuento` | Siempre 0 |
| `vencimiento` | Fecha actual (DD/MM/YYYY) |

---

## Lógica de Agrupación

Cada combinación única de `empresa` + `identificacion_tercero` (proveedor) genera una orden de compra independiente con su propio `documento_numero` incremental.

**Ejemplo:**
- IDs enviados: 5 registros
- Combinaciones únicas: 2 (IMPERIO + Proveedor A, IMPERIO + Proveedor B)
- Órdenes generadas: 2

---

## Ejemplo de Consumo (JavaScript)

```javascript
const exportarYGenerarOrdenes = async (ids) => {
  const response = await fetch('/api/v1/sugerido-compras/bulk-export', {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ ids })
  });
  
  const data = await response.json();
  
  // Procesar cada orden de compra
  for (const orden of data.ordenes_compra) {
    console.log(`Empresa: ${orden.encabezado.empresa}`);
    console.log(`Doc Número: ${orden.encabezado.documento_numero}`);
    console.log(`Productos: ${orden.detalles.length}`);
  }
  
  return data;
};
```

---

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| 400 | Lista de IDs vacía |
| 401 | Token inválido o expirado |
| 404 | No se encontraron registros con los IDs |
| 500 | Error interno del servidor |
