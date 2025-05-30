import os
import re
import subprocess
import shutil
import time

def savefig( filename : str, tex : str, data : list[str] ):
    file_type = os.path.basename( filename ).split( "." )[-1].lower()
    if file_type == "png":
        save_as_png( filename, tex, data )
    elif file_type == "pdf":
        save_as_pdf( filename, tex, data )
    elif file_type == "svg":
        save_as_svg( filename, tex, data )
    elif file_type == "tex":
        save_as_tex( filename, tex, data )
    elif file_type == "eps":
        save_as_eps( filename, tex, data )
    elif file_type == "jpeg":
        save_as_jpeg( filename, tex, data )
    elif file_type == "jpg":
        save_as_jpeg( filename.replace( ".jpg", "jpeg" ), tex, data )
    else:
        raise Exception( f"Unkown file extension: {file_type}. Supported extensions: .png, .pdf, .svg, .eps, .jpeg, .jpg, .tex" )

def compileCairo( filename : str, tex : str, data : list[str] ):
    file_ext = os.path.basename( filename ).split( "." )[-1].lower()
    dirname = os.path.dirname( filename )
    tmpdir  = os.path.join( dirname, ".tmp" )
    tmpflag = os.path.isdir( tmpdir )
    tmppdf  = os.path.join( tmpdir, "tmp.pdf" )

    save_as_pdf( tmppdf, tex, data )

    p = subprocess.run( [
        "pdftocairo",
        f"-{file_ext}",
        tmppdf
    ], shell=True, capture_output=True )
    
    if p.returncode != 0: raise Exception( p.stderr )
    if file_ext == "jpeg": file_ext = "jpg"

    for file in next( os.walk( tmpdir ) )[2]:
        if file_ext in file: break

    os.replace( os.path.join( tmpdir, file ), filename )
    shutil.rmtree( tmpdir, True )

def save_as_png( filename : str, tex : str, data : list[str] ):
    if tex:
        compileCairo( filename, tex, data )

def save_as_svg( filename : str, tex : str, data : list[str] ):
    if tex:
        compileCairo( filename, tex, data )

def save_as_eps( filename : str, tex : str, data : list[str] ):
    if tex:
        compileCairo( filename, tex, data )

def save_as_jpeg( filename : str, tex : str, data : list[str] ):
    if tex:
        compileCairo( filename, tex, data )

def save_as_pdf( filename : str, tex : str, data : list[str] ):
    if tex:
        dirname = os.path.dirname( filename )
        tmpdir  = os.path.join( dirname, ".tmp" )
        tmpflag = os.path.isdir( tmpdir )
        tmptex = os.path.join( tmpdir, f"tmp_{time.time()}" )

        if not tmpflag: os.makedirs( tmpdir, exist_ok=True )
        
        with open( f"{tmptex}.tex", "w" ) as pFile:
            pFile.write( tex )

        for i, dataset in enumerate( data ):
            with open( os.path.join( tmpdir, f"data_{i}.csv" ), "w" ) as pFile:
                pFile.write( dataset )
        
        p = subprocess.run( [
            "lualatex",
            "-enable-installer",
            "-shell-escape",
            "-interaction=nonstopmode",
            "-output-format=pdf",
            f"-output-directory={tmpdir}",
            f"-aux-directory={tmpdir}",
            f"{tmptex}.tex"
        ], shell=True, capture_output=True )
        
        if p.returncode != 0: raise Exception( p.stderr )
        
        os.replace( f"{tmptex}.pdf", filename )
        shutil.rmtree( tmpdir, True )

def save_as_tex( filename : str, tex : str, data : list[str] ):
    if tex:
        with open( filename, "w" ) as pFile:
            print( re.findall( r"\\begin{document\}\n*((?:.|\n)*)\n+\\end\{document\}", tex )[0], file=pFile )
        
        dirname = os.path.dirname( filename )
        for i, dataset in enumerate( data ):
            with open( os.path.join( dirname, f"data_{i}.csv" ), "w" ) as pFile:
                pFile.write( dataset )