proc infoproc mapping:

    Permet de voir la memory de notre programme

x/{nb d'instruction}{format} {adresse}

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
