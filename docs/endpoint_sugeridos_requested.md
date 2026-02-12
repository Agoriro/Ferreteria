# Endpoint: Obtener Sugeridos de Compras con Status "Requested"

## Información General

| Propiedad | Valor |
|-----------|-------|
| **Método** | `GET` |
| **URL** | `/api/v1/sugerido-compras/requested` |
| **Descripción** | Obtiene todos los registros de sugerido de compras con status "Requested", con filtro opcional por identificación del tercero |

---

## Parámetros de Query (Opcionales)

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `identificacion_tercero` | `string` | No | Filtra los resultados por la identificación del tercero/proveedor |

---

## Ejemplos de Uso

### Obtener todos los registros con status Requested
```
GET /api/v1/sugerido-compras/requested
```

### Filtrar por identificación del tercero
```
GET /api/v1/sugerido-compras/requested?identificacion_tercero=900123456
```

---

## Respuesta Exitosa (200 OK)

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "empresa": "IMPERIO",
      "fecha": "2026-01-15",
      "num_doc": "FC 001 12345",
      "proveedor": "Proveedor ABC",
      "identificacion_tercero": "900123456",
      "grupo3": "HERRAMIENTAS",
      "grupo4": "MANUALES",
      "grupo5": "MARTILLOS",
      "cod_prod": "PROD001",
      "descripcion": "Martillo de acero",
      "unidad_medida": "UND",
      "exist": 50.00,
      "exist_mc": 120.00,
      "cantidad_ventas_anterior": 200.00,
      "cantidad_ventas_actual": 180.00,
      "sugerido_compras": 45.00,
      "cantidad_a_pedir": 0.00,
      "proveedor1": "900123456 - Proveedor ABC",
      "proveedor2": "800654321 - Proveedor XYZ",
      "proveedor3": null,
      "proveedor4": null,
      "compras_en_el_periodo": 100.00,
      "total_entradas_en_el_periodo": 20.00,
      "ultima_fecha_compra": "2026-01-10",
      "ventas_en_el_periodo": 80.00,
      "total_salidas_en_el_periodo": 10.00,
      "ultima_fecha_venta": "2026-01-14",
      "saldo_actual": 20.00,
      "val_unit": 15000.00,
      "dcto": 1500.00,
      "val_neto": 16065.00,
      "precio1": 25000.00,
      "util_1": 35.74,
      "precio2": 22000.00,
      "util_2": 26.98,
      "cantidad_proveedor": 0.00,
      "valor_unitario_proveedor": 0.00,
      "status": "Requested",
      "created_at": "2026-01-15T10:30:00Z"
    }
  ],
  "total": 1
}
```

---

## Ejemplo de Implementación en Frontend (TypeScript/JavaScript)

### Interfaz de Tipos
```typescript
interface SugeridoComprasResponse {
  id: string;
  empresa: string;
  fecha: string | null;
  num_doc: string | null;
  proveedor: string | null;
  identificacion_tercero: string | null;
  grupo3: string | null;
  grupo4: string | null;
  grupo5: string | null;
  cod_prod: string;
  descripcion: string | null;
  unidad_medida: string | null;
  exist: number;
  exist_mc: number;
  cantidad_ventas_anterior: number;
  cantidad_ventas_actual: number;
  sugerido_compras: number;
  cantidad_a_pedir: number;
  proveedor1: string | null;
  proveedor2: string | null;
  proveedor3: string | null;
  proveedor4: string | null;
  compras_en_el_periodo: number;
  total_entradas_en_el_periodo: number;
  ultima_fecha_compra: string | null;
  ventas_en_el_periodo: number;
  total_salidas_en_el_periodo: number;
  ultima_fecha_venta: string | null;
  saldo_actual: number;
  val_unit: number;
  dcto: number;
  val_neto: number;
  precio1: number;
  util_1: number;
  precio2: number;
  util_2: number;
  cantidad_proveedor: number;
  valor_unitario_proveedor: number;
  status: 'Created' | 'Requested' | 'Processed' | 'Exported';
  created_at: string;
}

interface SugeridoComprasListResponse {
  items: SugeridoComprasResponse[];
  total: number;
}
```

### Función de Servicio
```typescript
const API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * Obtiene los sugeridos de compras con status "Requested"
 * @param identificacionTercero - Opcional: filtra por identificación del tercero
 */
async function getSugeridosRequested(
  identificacionTercero?: string
): Promise<SugeridoComprasListResponse> {
  const params = new URLSearchParams();
  
  if (identificacionTercero) {
    params.append('identificacion_tercero', identificacionTercero);
  }
  
  const queryString = params.toString();
  const url = `${API_BASE_URL}/sugerido-compras/requested${queryString ? '?' + queryString : ''}`;
  
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      // Agregar token si es necesario
      // 'Authorization': `Bearer ${token}`
    }
  });
  
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }
  
  return response.json();
}
```

### Ejemplo de Uso en React
```tsx
import { useState, useEffect } from 'react';

function SugeridosRequestedList() {
  const [sugeridos, setSugeridos] = useState<SugeridoComprasResponse[]>([]);
  const [filtroTercero, setFiltroTercero] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const cargarSugeridos = async () => {
    setLoading(true);
    try {
      const data = await getSugeridosRequested(filtroTercero || undefined);
      setSugeridos(data.items);
    } catch (error) {
      console.error('Error al cargar sugeridos:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarSugeridos();
  }, []);

  return (
    <div>
      <input
        type="text"
        placeholder="Filtrar por ID Tercero"
        value={filtroTercero}
        onChange={(e) => setFiltroTercero(e.target.value)}
      />
      <button onClick={cargarSugeridos}>Buscar</button>
      
      {loading ? (
        <p>Cargando...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Código</th>
              <th>Descripción</th>
              <th>Proveedor</th>
              <th>Sugerido</th>
            </tr>
          </thead>
          <tbody>
            {sugeridos.map((item) => (
              <tr key={item.id}>
                <td>{item.cod_prod}</td>
                <td>{item.descripcion}</td>
                <td>{item.proveedor}</td>
                <td>{item.sugerido_compras}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
```

---

## Estados Disponibles (StatusSugerido)

| Estado | Descripción |
|--------|-------------|
| `Created` | Registro recién generado |
| `Requested` | Registro solicitado/enviado |
| `Processed` | Registro procesado |
| `Exported` | Registro exportado |
