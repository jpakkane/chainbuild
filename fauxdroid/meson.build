project('fauxdroid', 'c')

if get_option('build_java')
    add_languages('java')
    javaprog = jar('faux', 'com/mesonbuild/Faux.java',
        main_class : 'com.mesonbuild.faux',
        install : true,
        install_dir : get_option('bindir'))
endif

shared_library('faux', 'faux.c',
    install: true)
