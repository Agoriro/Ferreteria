# Endpoint: Actualización Masiva de Sugeridos con Datos del Proveedor

## Información General

| Propiedad | Valor |
|-----------|-------|
| **Método** | `PATCH` |
| **URL** | `/api/v1/sugerido-compras/bulk-update-proveedor` |
| **Descripción** | Actualiza múltiples registros de sugerido de compras con los datos del proveedor y cambia su status a "Processed" |

---

## Request Body

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "cantidad_proveedor": 100.00,
      "valor_unitario_proveedor": 15000.00
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "cantidad_proveedor": 50.00,
      "valor_unitario_proveedor": 8500.50
    }
  ]
}
```

### Campos del Item

| Campo | Tipo | Requerido | Validación | Descripción |
|-------|------|-----------|------------|-------------|
| `id` | `UUID` | Sí | - | ID del registro a actualizar |
| `cantidad_proveedor` | `number` | Sí | Mayor a 0 | Cantidad ofrecida por el proveedor |
| `valor_unitario_proveedor` | `number` | Sí | Mayor a 0 | Valor unitario ofrecido por el proveedor |

### Validaciones Automáticas

- ✅ `cantidad_proveedor` debe ser **mayor a 0** (no puede ser 0 ni negativo)
- ✅ `valor_unitario_proveedor` debe ser **mayor a 0** (no puede ser 0 ni negativo)
- ✅ La lista `items` debe tener **al menos 1 elemento**

---

## Respuesta Exitosa (200 OK)

```json
{
  "message": "Registros actualizados correctamente",
  "updated_count": 2,
  "updated_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "660e8400-e29b-41d4-a716-446655440001"
  ]
}
```

---

## Errores de Validación (422 Unprocessable Entity)

Si algún campo no cumple con las validaciones:

```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "items", 0, "cantidad_proveedor"],
      "msg": "Input should be greater than 0",
      "input": 0,
      "ctx": {"gt": 0}
    }
  ]
}
```

---

## Ejemplo de Implementación en Frontend (TypeScript)

### Interfaces

```typescript
interface SugeridoProveedorItem {
  id: string;
  cantidad_proveedor: number;
  valor_unitario_proveedor: number;
}

interface SugeridoBulkUpdateRequest {
  items: SugeridoProveedorItem[];
}

interface SugeridoBulkUpdateResponse {
  message: string;
  updated_count: number;
  updated_ids: string[];
}
```

### Función de Servicio

```typescript
const API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * Actualiza múltiples sugeridos con datos del proveedor
 * @param items - Lista de items a actualizar
 */
async function bulkUpdateSugeridosProveedor(
  items: SugeridoProveedorItem[]
): Promise<SugeridoBulkUpdateResponse> {
  
  // Validación cliente antes de enviar
  for (const item of items) {
    if (item.cantidad_proveedor <= 0) {
      throw new Error('cantidad_proveedor debe ser mayor a 0');
    }
    if (item.valor_unitario_proveedor <= 0) {
      throw new Error('valor_unitario_proveedor debe ser mayor a 0');
    }
  }
  
  const response = await fetch(`${API_BASE_URL}/sugerido-compras/bulk-update-proveedor`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      // 'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ items })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(JSON.stringify(error.detail));
  }
  
  return response.json();
}
```

### Ejemplo de Uso en React

```tsx
import { useState } from 'react';

function ActualizarProveedorForm() {
  const [sugeridos, setSugeridos] = useState<SugeridoProveedorItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SugeridoBulkUpdateResponse | null>(null);

  const handleUpdate = async () => {
    // Validar que todos tengan valores > 0
    const invalidos = sugeridos.filter(
      s => s.cantidad_proveedor <= 0 || s.valor_unitario_proveedor <= 0
    );
    
    if (invalidos.length > 0) {
      alert('Todos los campos deben ser mayores a 0');
      return;
    }
    
    setLoading(true);
    try {
      const response = await bulkUpdateSugeridosProveedor(sugeridos);
      setResult(response);
      alert(`${response.updated_count} registros actualizados correctamente`);
    } catch (error) {
      console.error('Error:', error);
      alert('Error al actualizar los registros');
    } finally {
      setLoading(false);
    }
  };

  // ... renderizado del formulario
}
```

---

## Flujo de Trabajo

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  GET /requested  │────▶│  Usuario edita   │────▶│  PATCH /bulk-    │
│  Status:Requested│     │  cantidad y      │     │  update-proveedor│
│                  │     │  valor_unitario  │     │  Status:Processed│
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

1. Obtener registros con status "Requested" usando `GET /requested`
2. El usuario ingresa `cantidad_proveedor` y `valor_unitario_proveedor` para cada item
3. Enviar los items actualizados a `PATCH /bulk-update-proveedor`
4. Los registros se actualizan y su status cambia a "Processed"
