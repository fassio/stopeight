def test_Sequential():
    from PyQt5.QtWidgets import QApplication,QMainWindow
    from stopeight.util.editor.modules import legacy
    from stopeight.util.parser import process_directory
    import stopeight.logging as log
    log.disable(log.WARNING)
    lines = process_directory('stopeight-clibs/legacy/tests','.sp',legacy._parse_file,legacy.stroke_sequential,filename='Sequential.out',drawResize=False)

def test_Parallel():
    from PyQt5.QtWidgets import QApplication,QMainWindow
    from stopeight.util.editor.modules import legacy
    from stopeight.util.parser import process_directory
    import stopeight.logging as log
    log.disable(log.WARNING)
    lines = process_directory('stopeight-clibs/legacy/tests','.sp',legacy._parse_file,legacy.stroke_parallel,filename='Parallel.out',drawResize=False)