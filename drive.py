from google.oauth2 import service_account
from googleapiclient.discovery import build

DRIVE_SCOPE = ['https://www.googleapis.com/auth/drive']
KEY = 'keys/key.json'

drive_creds = service_account.Credentials.from_service_account_file(KEY, scopes=DRIVE_SCOPE)
drive_service2 = build("drive", "v2", credentials=drive_creds)
drive_service = build("drive", "v3", credentials=drive_creds)

# --------------------------------
new_permi= {
    'type':'user',
    'role':'writer',
    'emailAddress':'email_to_add_permission',
    "pendingOwner": True
}
new_permi2= {
  "id": "123....",
  "type": "user",
  "emailAddress": 'email_to_add_permission',
  "role": "owner",
  "pendingOwner": True
}
# --------------------------------

# CREANDO PERMISO CON DRIVE PARA UN ARCHIVO --------------------------------
# permissio = drive_service.permissions().create(
#     fileId= 'FILE_ID_1234..',
#     # transferOwnership= True,
#     # permissionId = 234...",
#     emailMessage = "Esta es una prueba de transferencia de propiedad",
#     # moveToNewOwnersRoot = True,
#     sendNotificationEmail = True,
#     body=new_permi
# ).execute()
# print(permissio)
# {'kind': 'drive#permission', 'id': '123....', 'type': 'user', 'role': 'writer'}


# LISTANDO PERMISOS CON DRIVE PARA UN ARCHIVO --------------------------------
# permissio = drive_service.permissions().list(
#     fileId= 'FILE_ID_1234..',
# ).execute()
# print(permissio)
# {'kind': 'drive#permissionList', 'permissions': [{'id': '123....', 'type': 'user', 'kind': 'drive#permission', 'role': 'writer'}, {'id': '234...', 'type': 'user', 'kind': 'drive#permission', 'role': 'owner'}]}

# ACTUALIZAR PERMISO CON DRIVE PARA UN ARCHIVO --------------------------------
# permissio = drive_service.permissions().update(
#    fileId= 'FILE_ID_1234..',
#    permissionId = "123....",
#    removeExpiration = False,
#    transferOwnership = True,
#    body = body,
# ).execute()
# print(permissio)

# OBTENEMOS INFORMACION DE UN PERMISO MEDIANTE SU ID --------------------------------
# permissio = drive_service.permissions().get(
#    fileId= 'FILE_ID_1234..',
#    permissionId = "123....",
#    body=new_permi2
#).execute()
#print(permissio)

# BORRAMOS UN PERMISO MEDIANTE SU ID --------------------------------
# permissio = drive_service.permissions().delete(
#    fileId= 'FILE_ID_1234..',
#    permissionId = "123....",
#).execute()
#print(permissio)

# INSERTAMOS UN PERMISO EN UN ARCHIVO (v2) --------------------------------
# permissio = drive_service2.permissions().insert(
#    fileId= 'FILE_ID_1234..',
#    transferOwnership= True,
#    emailMessage = "Esta es ....",
#    moveToNewOwnersRoot = True,
#    sendNotificationEmails = True,
#    pendingOwner=True,
#    useDomainAdminAccess= True,
#    body=new_permi2
# ).execute()
# print(permissio)

# LISTADO DE ARCHIVOS CREADOS Y/O CON ACCESO --------------------------------
files = drive_service.files().list().execute()
print(files)
# {'files': [{'kind': 'drive#file', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'id': 'FILE_ID_1234..', 'name': 'mySheets'}, {'kind': 'drive#file', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'id': '10-XhAKVGEbLTzjN-KDNc5jVi83itkvi5Brda4PVxZp8', 'name': 'Primer-Projecto'}]}

# ACTUALIZACION DE PERMISOS PARA UN ARCHIVO CON DRIVE --------------------------------
# result = drive_service.files().update(
#     fileId= "FILE_ID_1234..",
#     body = {"permissionIds":[permissio['id']]}
# ).execute()
# print(result)

# CONCLUSION - NO SE PUEDE TRANSFERIR LA PROPIEDAD DE UN ARCHIVO SHEETS CREADA CON UNA CUENTA DE SERVICIO