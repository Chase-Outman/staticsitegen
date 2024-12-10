import shutil, os

from page_generator import generate_page, generate_pages_recursive

def copy_dir_to_new_dir(source, dest):    
        #if the destination path exsist, then delete it to ensure a fresh copy of files    
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    if os.path.isfile(source):
        shutil.copy(source, dest)
        return

    dir_list = os.listdir(source)
    
    for e in dir_list:
        spath = os.path.join(source, e)
        dpath = os.path.join(dest, e)
        if os.path.isfile(spath):
            copy_dir_to_new_dir(spath, dest)    
        else:
            copy_dir_to_new_dir(spath, dpath)
    
    

def main():
#   copy_dir_to_new_dir("./static", "./public")
#    generate_page("./content/index.md", "./template.html", "./public/index.html")

    generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()