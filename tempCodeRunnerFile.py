from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastai.learner import load_learner
from fastai.vision.core import PILImage
from fastapi import FastAPI, Query, HTTPException, File, UploadFile
from io import BytesIO