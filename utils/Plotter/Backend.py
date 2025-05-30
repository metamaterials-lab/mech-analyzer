CFGLaTeXRuntime = True

if CFGLaTeXRuntime:
    from utils.LaTeX.LaTeXPlot import LaTeXPlot
    plt = LaTeXPlot()
else:
    from matplotlib import pyplot as plt
    plt.rcParams.update({
        "font.family": "Cambria"
    })