from typing import Annotated

from fastapi import Depends


from config.uow_conf import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

