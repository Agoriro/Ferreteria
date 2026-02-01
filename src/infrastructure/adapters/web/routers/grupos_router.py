"""
Router para endpoints de Grupos (Tres, Cuatro, Cinco).
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from uuid import UUID

from domain.schemas.grupos_schema import (
    GruposTresCreate, GruposTresUpdate, GruposTresResponse, GruposTresListResponse,
    GruposCuatroCreate, GruposCuatroUpdate, GruposCuatroResponse, GruposCuatroListResponse,
    GruposCincoCreate, GruposCincoUpdate, GruposCincoResponse, GruposCincoListResponse,
    GruposCombinedResponse
)
from application.use_cases.grupos_use_case import (
    GruposTresUseCase,
    GruposCuatroUseCase,
    GruposCincoUseCase
)
from infrastructure.adapters.web.dependencies import (
    get_grupos_tres_use_case,
    get_grupos_cuatro_use_case,
    get_grupos_cinco_use_case
)

router = APIRouter(tags=["Grupos"])


# ============== Endpoint Combinado ==============

@router.get("/grupos", response_model=GruposCombinedResponse)
async def get_all_grupos(
    use_case_tres: GruposTresUseCase = Depends(get_grupos_tres_use_case),
    use_case_cuatro: GruposCuatroUseCase = Depends(get_grupos_cuatro_use_case),
    use_case_cinco: GruposCincoUseCase = Depends(get_grupos_cinco_use_case)
):
    """Obtener todos los grupos combinados en un solo objeto."""
    # Obtener todos los registros (limit alto para obtener todos)
    grupos_tres = await use_case_tres.get_all(skip=0, limit=10000)
    grupos_cuatro = await use_case_cuatro.get_all(skip=0, limit=10000)
    grupos_cinco = await use_case_cinco.get_all(skip=0, limit=10000)
    
    return GruposCombinedResponse(
        Grupo_Tres=[g.grupo_tres for g in grupos_tres.items],
        Grupo_Cuatro=[g.grupo_cuatro for g in grupos_cuatro.items],
        Grupo_Cinco=[g.grupo_cinco for g in grupos_cinco.items]
    )


# ============== Grupos Tres ==============

@router.get("/grupos-tres", response_model=GruposTresListResponse)
async def get_grupos_tres(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    use_case: GruposTresUseCase = Depends(get_grupos_tres_use_case)
):
    """Obtener lista de Grupos Tres."""
    return await use_case.get_all(skip, limit)


@router.get("/grupos-tres/{id}", response_model=GruposTresResponse)
async def get_grupo_tres(
    id: UUID,
    use_case: GruposTresUseCase = Depends(get_grupos_tres_use_case)
):
    """Obtener un Grupo Tres por ID."""
    result = await use_case.get_by_id(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado"
        )
    return result


@router.post("/grupos-tres", response_model=GruposTresResponse, status_code=status.HTTP_201_CREATED)
async def create_grupo_tres(
    data: GruposTresCreate,
    use_case: GruposTresUseCase = Depends(get_grupos_tres_use_case)
):
    """Crear un nuevo Grupo Tres."""
    try:
        return await use_case.create(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/grupos-tres/{id}", response_model=GruposTresResponse)
async def update_grupo_tres(
    id: UUID,
    data: GruposTresUpdate,
    use_case: GruposTresUseCase = Depends(get_grupos_tres_use_case)
):
    """Actualizar un Grupo Tres."""
    try:
        result = await use_case.update(id, data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grupo no encontrado"
            )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/grupos-tres/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grupo_tres(
    id: UUID,
    use_case: GruposTresUseCase = Depends(get_grupos_tres_use_case)
):
    """Eliminar un Grupo Tres."""
    deleted = await use_case.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado"
        )


# ============== Grupos Cuatro ==============

@router.get("/grupos-cuatro", response_model=GruposCuatroListResponse)
async def get_grupos_cuatro(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    use_case: GruposCuatroUseCase = Depends(get_grupos_cuatro_use_case)
):
    """Obtener lista de Grupos Cuatro."""
    return await use_case.get_all(skip, limit)


@router.get("/grupos-cuatro/{id}", response_model=GruposCuatroResponse)
async def get_grupo_cuatro(
    id: UUID,
    use_case: GruposCuatroUseCase = Depends(get_grupos_cuatro_use_case)
):
    """Obtener un Grupo Cuatro por ID."""
    result = await use_case.get_by_id(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado"
        )
    return result


@router.post("/grupos-cuatro", response_model=GruposCuatroResponse, status_code=status.HTTP_201_CREATED)
async def create_grupo_cuatro(
    data: GruposCuatroCreate,
    use_case: GruposCuatroUseCase = Depends(get_grupos_cuatro_use_case)
):
    """Crear un nuevo Grupo Cuatro."""
    try:
        return await use_case.create(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/grupos-cuatro/{id}", response_model=GruposCuatroResponse)
async def update_grupo_cuatro(
    id: UUID,
    data: GruposCuatroUpdate,
    use_case: GruposCuatroUseCase = Depends(get_grupos_cuatro_use_case)
):
    """Actualizar un Grupo Cuatro."""
    try:
        result = await use_case.update(id, data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grupo no encontrado"
            )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/grupos-cuatro/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grupo_cuatro(
    id: UUID,
    use_case: GruposCuatroUseCase = Depends(get_grupos_cuatro_use_case)
):
    """Eliminar un Grupo Cuatro."""
    deleted = await use_case.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado"
        )


# ============== Grupos Cinco ==============

@router.get("/grupos-cinco", response_model=GruposCincoListResponse)
async def get_grupos_cinco(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    use_case: GruposCincoUseCase = Depends(get_grupos_cinco_use_case)
):
    """Obtener lista de Grupos Cinco."""
    return await use_case.get_all(skip, limit)


@router.get("/grupos-cinco/{id}", response_model=GruposCincoResponse)
async def get_grupo_cinco(
    id: UUID,
    use_case: GruposCincoUseCase = Depends(get_grupos_cinco_use_case)
):
    """Obtener un Grupo Cinco por ID."""
    result = await use_case.get_by_id(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado"
        )
    return result


@router.post("/grupos-cinco", response_model=GruposCincoResponse, status_code=status.HTTP_201_CREATED)
async def create_grupo_cinco(
    data: GruposCincoCreate,
    use_case: GruposCincoUseCase = Depends(get_grupos_cinco_use_case)
):
    """Crear un nuevo Grupo Cinco."""
    try:
        return await use_case.create(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/grupos-cinco/{id}", response_model=GruposCincoResponse)
async def update_grupo_cinco(
    id: UUID,
    data: GruposCincoUpdate,
    use_case: GruposCincoUseCase = Depends(get_grupos_cinco_use_case)
):
    """Actualizar un Grupo Cinco."""
    try:
        result = await use_case.update(id, data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grupo no encontrado"
            )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/grupos-cinco/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grupo_cinco(
    id: UUID,
    use_case: GruposCincoUseCase = Depends(get_grupos_cinco_use_case)
):
    """Eliminar un Grupo Cinco."""
    deleted = await use_case.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado"
        )
