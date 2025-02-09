from fastapi import FastAPI, File, UploadFile, HTTPException
import os # for handling file directories
import shutil # for copying file data

UPLOAD_DIR = "uploads"

# create a fastapi instance
app = FastAPI()

# /*********** CODE TO UPLOAD FILES AT ONCE***************************/
@app.post("/small_files_upload")
async def small_files(file: UploadFile = File(...)):
    
    # path to save the uploaded file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    
    # Open teh file in write-binary mode and save it
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"Filename": file.filename, "message": "The file uploaded successfully"}

# /*********** CODE TO UPLOAD LARGE FILES IN CHUNKS***************************/

@app.post("large_files")
async def large_files(file: UploadFile = File(...)):
    file_size = 0
    
    max_size = 1024 * 1024 * 1024 # setting max size to 1gb
    
    # path to ave the uploaded file
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            file_size += len(chunk)
            if file_size > max_size:
               buffer.close()
               os.remove(file_location)
               raise HTTPException(status_code = 413, detail = "File too large (max 1GB)")
            buffer.write(chunk)
            
    return {"filename": file.filename, "message": "The file uploaded successfully"}

    