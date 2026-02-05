info proc mappings:

    Permet de voir la memory de notre programme

x/{nb d'instruction}i {adresse}

    Permet d'examiner une adresse

set *({adresse}) = {value}

    permet de changer une valeur en memoire

set {reg} = {value}

    permet de changer une valeur dans un register

set [{cast}] {addr/reg} = {value}

    permet de caster la valeur en {cast} et de la setter

b *($base + offset)
    
    ajoute un breakpoint au offset

d breakpoints
    
    supprime les breakpoints


r < {filepath} 

    permet de run en passant un file d'input

run < <(printf '[ToInject]')

    permet de run en injectant un input dans stdin 

command
    permet de faire une commande quand le breakpoint est atteint
    
    fini avec end

    ex:
    command 1
        set $rdi = 0xdeadbeef
        echo "hello world"
        x/10x $rdi
    end