# IIS - Zelny Trh
   
Úkolem zadání je vytvořit jednoduchý informační systém pro nabídku ovoce a zeleniny vypěstovaných farmáři. Každé nabízené ovoce/zeleninu je možné zařadit právě do jedné kategorie plodin. Kategorie mají stromový charakter (např. plodina > zelenina > rajče > rajče Tomino). Každá kategorie dále předepisuje další dodatečné atributy (povinné i volitelné), jejichž hodnoty se váží k vytvořené nabídce (např. cena/kg, cena/kus, místo původu, dostupné množství apod.). Různé druhy plodin tedy mohou být charakterizovány množinou odlišných atributů. Nabízené ovoce/zelenina mohou být nabízeny přímo k prodeji nebo k samosběru. Samosběr je časově ohraničená událost, která se koná na předem daném místě a kterou si uživatelé mohou přidat do seznamu svých událostí. V systému budou konkrétně vystupovat následující role:

        administrátor:
            spravuje uživatele, jako jediný vytváří moderátory

        moderátor
            spravuje kategorie plodin a jejich atributů
            schvaluje návrhy kategorií uživateli

        registrovaný uživatel:
            edituje svůj profil
            navrhuje nové kategorie plodin
            vkládá nabídky produktů do kategorií - stává se farmářem
                spravuje své nabídky
                aktualizuje dostupné množství nabízených plodin
                vyřizuje objednávky
                plánuje samosběry
            objednává produkty - stává se zákazníkem
                provádí objednávky
                hodnotí zakoupené produkty
        neregistrovaný:
            vyhledává a prohlíží nabídku ovoce a zeleniny (filtruje dle kategorií a atributů)
            prochází farmáře a jejich nabídky
            porovnává ceny pro jednotlivé kategorie

    Náměty na rozšíření:

        uživatelsky přívětivé porovnávání cen různých farmářů, uživatelské hodnocení farmářů, …
        dle vlastní fantazie, popište v dokumentaci…

    Dále postupujte dle všeobecného zadání: 
   https://moodle.vut.cz/mod/page/view.php?id=238239

