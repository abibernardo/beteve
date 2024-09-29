import streamlit as st

st.markdown("""
<h1 style='text-align: center; font-size: 60px; font-family: Palatino;'>
BETEVÊ
</h1>
""", unsafe_allow_html=True)
st.divider()
# Exibindo a imagem logo abaixo do título
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style='text-align: center;'>
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_QyOJeldPSl2Afu4VYYKYpeOHC7GMbWxftw&s" 
            style="width: 300px; height: 350px; object-fit: cover;">
        </div>
        """, unsafe_allow_html=True)
    st.write(" ")
    st.markdown("""
                <div style='text-align: center;'>
                    <img src="https://baxterandthebear.com/cdn/shop/products/successionpreview_400x.jpg?v=1648683927" 
                    style="width: 300px; height: 350px; object-fit: cover;">
                </div>
                """, unsafe_allow_html=True)
    st.write(" ")
    st.markdown("""
                    <div style='text-align: center;'>
                        <img src="https://cdn11.bigcommerce.com/s-yzgoj/images/stencil/1280x1280/products/2898769/5925501/MOVGB42273__95963.1679574735.jpg?c=2" 
                        style="width: 300px; height: 350px; object-fit: cover;">
                    </div>
                    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div style='text-align: center;'>
            <img src="https://m.media-amazon.com/images/M/MV5BMjA0NTUxMjY1OV5BMl5BanBnXkFtZTcwNjI2OTMzMQ@@._V1_QL75_UY281_CR0,0,190,281_.jpg" 
            style="width: 300px; height: 350px; object-fit: cover;">
        </div>
        """, unsafe_allow_html=True)
    st.write(" ")
    st.markdown("""
            <div style='text-align: center;'>
                <img src="https://down-br.img.susercontent.com/file/br-11134207-7qukw-liisz1wf8sadfe" 
                style="width: 300px; height: 350px; object-fit: cover;">
            </div>
            """, unsafe_allow_html=True)
    st.write(" ")
    st.markdown("""
                    <div style='text-align: center;'>
                        <img src="https://m.media-amazon.com/images/M/MV5BOGIwYzNmYTktZWExZC00MzAyLTk4NTItODgwZmIyNWZhNDEyXkEyXkFqcGc@._V1_.jpg" 
                        style="width: 300px; height: 350px; object-fit: cover;">
                    </div>
                    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style='text-align: center;'>
            <img src="https://br.web.img2.acsta.net/pictures/22/02/17/22/59/4379186.jpg" 
            style="width: 300px; height: 350px; object-fit: cover;">
        </div>
        """, unsafe_allow_html=True)
    st.write(" ")
    st.markdown("""
            <div style='text-align: center;'>
                <img src="https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p24090_v_v10_ag.jpg" 
                style="width: 300px; height: 350px; object-fit: cover;">
            </div>
            """, unsafe_allow_html=True)
    st.write(" ")
    st.markdown("""
                    <div style='text-align: center;'>
                        <img src="https://m.media-amazon.com/images/M/MV5BMTQ1MTY2MTY2Nl5BMl5BanBnXkFtZTcwMDg1ODYwNA@@._V1_.jpg" 
                        style="width: 300px; height: 350px; object-fit: cover;">
                    </div>
                    """, unsafe_allow_html=True)


st.write("   ")
st.divider()
st.write("   ")
st.markdown("""
    <h1 style='text-align: center; font-size: 30px; font-family: Palatino;'>
        Opiniões, críticas, elogios e palpites sobre televisão
    </h1>
    """, unsafe_allow_html=True)
st.divider()
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0;">
        <div>
            <h3><b>Sobre Twin Peaks:</b> De fora pra dentro.</h3>
        </div>
        <div>
            <img src="https://s2.glbimg.com/aVCeHUpHz-sfAESOQfK_uNwjDE0=/smart/e.glbimg.com/og/ed/f/original/2014/10/07/meanwhile.jpg" 
            style="width: 250px; height: 180px; margin-left: 20px;">
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
if st.button("Ler mais", key='Laura'):
    st.markdown("""
        Um pescador junta seu equipamento, despede-se da esposa, e vai em direção a um rio próximo. 
        Antes de começar a pescar, avista um objeto estranho às margens. Corre de volta para sua casa, 
        liga para a polícia e anuncia: **"She is dead... Wrapped in plastic"**.

        É assim que Twin Peaks apresenta sua principal personagem: como um cadáver.

        O agente Dale Cooper é o encarregado de investigar o crime, e são por seus olhos que conhecemos o mundo de Twin Peaks. 
        Assistimos como a tragédia abala as estruturas da então (aparentemente) pacata cidade. 
        Por meio da investigação, conhecemos camadas e mais camadas de cada personagem e de suas relações. 
        Entendemos os dramas, e vemos múltiplos enredos serem movidos pela angustiante pergunta gritando em segundo plano: 
        **Quem matou Laura Palmer?**

        **SUBVERSÕES**  
        Twin Peaks se inicia com a aparência de um mistério policial clássico:
        uma investigação de assassinato conduzida por um detetive carismático, e personagens misteriosos potencialmente suspeitos. 
        Aos poucos, porém, vamos percebendo uma subversão gigantesca desse gênero: trata-se de uma narrativa muito mais subjetiva e abstrata do que essa - é uma série Lynchiana, afinal.

        O surrealismo é introduzido no terceiro episódio da série, numa das cenas mais marcantes e aterrorizantes da história da televisão: 
        em um sonho, agente Cooper é idoso, sentado numa sala toda vermelha. 
        A sua frente, estão sentadas duas pessoas: um homem muito pequeno, com um terno vermelho e olhos pretos. 
        Ao seu lado, Laura Palmer. Nesse quarto vermelho, o áudio e as imagens são gravadas ao contrário, 
        e há um clima etéreo no ar. O homem pequeno, com uma voz perturbadora e com as palavras soando ao contrário, diz: 
        **"De onde nós somos, os pássaros cantam uma canção bonita, e há sempre música no ar. Ela não parece a Laura Palmer?".** 
        Na sequência, Laura Palmer diz: **"Sinto que conheço ela. Mas às vezes, meus braços dobram pra trás".** 
        Uma música começa, o homem pequeno se levanta e começa a dançar. Laura Palmer, sorrindo, se levanta e caminha até o agente Cooper. 
        Se abaixa, e cochicha algo em seu ouvido.
    """)

    st.image(
        "https://static.wikia.nocookie.net/twinpeaks/images/0/0f/MFAPsitting.jpg",
        caption="'The Man from Another Place'",
        width=400
    )

    st.markdown("""
        **AS CAMADAS**

        Sonhos e intuições espirituais, então, passam a fazer parte da investigação. 
        Um astral esotérico permeia a história, permitindo que David Lynch mergulhe em representações cada vez mais abstratas de traumas, 
        arrependimentos e autodestruição. Por meio dessas fortes abstrações, da investigação do assassinato e das relações que os personagens 
        tinham com Laura, vai se construindo uma personagem densa, complexa, subjetiva e real, 
        **sem que ela apareça na tela** - de fora pra dentro.

        Esse é o coração de Twin Peaks: a fortíssima sensação
        de que **a narrativa é assombrada pela sua protagonista**. 
        Em muitos momentos, é um sentimento aterrorizante - diga-se de passagem. Como Donna desabafa em frente ao túmulo de Laura Palmer: 'É quase como se não tivessem te enterrado fundo o suficiente'.  
    """)
st.divider()
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0;">
        <div>
            <h3><b>Sobre Hacks:</b> O que é se reinventar? </h3>
        </div>
        <div>
            <img src="https://www.rollingstone.com/wp-content/uploads/2024/09/hacks-comedy-win.jpg?w=1581&h=1054&crop=1" 
            style="width: 250px; height: auto; margin-left: 20px;">
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
if st.button("Ler mais", key='hacks'):
    st.markdown("""
        Nos Emmys de 2024, houve uma surpresa agradabilíssima na categoria de comédia: o prêmio de _Melhor Série_ foi para **Hacks**! 
        Surpresa grande para as casas de aposta - mas não para mim.

        Após dois Emmys de Melhor Roteiro em suas duas primeiras temporadas, os criadores Lucia Aniello, Paul W. Downs (Jimmy!) 
        e Jen Statsky finalmente venceram o prêmio principal com uma espetacular terceira temporada, 
        juntamente com seu terceiro Emmy de Melhor Roteiro com o episódio **mais bem avaliado da história da série**, _Bulletproof_.

        Isso é espantoso. Como uma série que teve que se reinventar em TODAS as transições de temporada, não só conseguiu 
        manter seu prestígio, como elevou o nível? E o quão difícil isso é?

        **GOLAÇO ATRÁS DE GOLAÇO**  
        Rememorando, Hacks iniciou com a proposta de uma parceria aparentemente incompatível: uma jovem roteirista trabalhando para uma estrela 
        consagrada da comédia na terceira idade. A proposta funcionou. Jean Smart e Hannah Einbinder - Deborah e Ava - mostraram-se impecáveis.

        Numa relação de mutualismo igualmente fofo e hilário, Deborah e Ava, aos poucos, aceitam aprender uma com a outra, 
        e trabalham juntas para reerguer a carreira de Deborah que, ao longo do seu convívio com a colega, se desprende do seu estilo antigo 
        e aceita ser uma comediante mais flexível.

        Na segunda temporada, Deborah decide fazer um tour de shows, e leva Ava como roteirista. 
        O convívio torna-se cada vez mais complexo, e os efeitos que uma tem na outra - tanto os positivos, quanto os tóxicos - 
        ficam gradualmente mais evidentes, simultaneamente dando profundidade à relação das duas e proporcionando trocas absolutamente hilárias.

        Na terceira temporada, Hacks passou pela sua segunda transição notável de formato: os shows de comédia acabaram, 
        e o coração da temporada foi a disputa de Deborah pelo cargo de apresentadora do Saturday Night Live - trabalho de seus sonhos. 
        Ava aceita ajudar Deborah, e o resultado foi mais uma temporada absolutamente espetacular - inclusive, talvez, a melhor.
    """)

    # Inserir a imagem associada ao texto
    st.image("https://rollingstone.com.br/media/_versions/2024/03/hacks-imagem-max-divulgacao_widelg.jpg",
             caption="Deborah e Ava (esse ep é sensacional)")

    # Continuação do texto
    st.markdown("""
        É raríssimo ver uma série (especialmente de comédia) passar por mudanças significativas em seu formato e ainda assim manter a excelência. 
        Nos tempos recentes, o único comparativo que consigo pensar é em _White Lotus_ - duas temporadas de altíssimo nível, 
        com propostas completamente diferentes uma da outra.

        Ainda assim, acho o caso de Hacks ainda mais impressionante. Não houve uma mudança total na série, ou uma adição gigantesca de elenco, 
        ou uma perda de linearidade. A série passou da forma mais orgânica possível pelas mudanças que faziam sentido, 
        se adaptou e - assim como nossa querida Deborah fez - se reinventou, de verdade, no mais alto nível. 

        Aguardo ansioso pela quarta temporada!
    """)
st.divider()
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0;">
        <div>
            <h3><b>De Arrested Development a Trailer Park Boys:</b> extremos do humor</h3>
        </div>
        <div>
            <img src="https://medias.spotern.com/spots/w640/194/194928-1555692527.jpg" 
            style="width: 450px; height: 200; margin-left: 20px;">
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
if st.button("Ler mais", key='comedia'):
    st.markdown("""
O que te faz dar risada? Trocadilhos, Hamilton, vídeo-cassetadas ou o Danilo Gentili?

São poucas as coisas mais relativas do que o humor, e por isso a comédia é um estilo tão delicado de se trabalhar. Para cada série genuinamente engraçada, vão-se cem fracassos varridos para debaixo do tapete pelas plataformas de streamings. Existem muitas comédias boas, mas qual foi a última que te fez gargalhar?

Pessoalmente, apenas três séries me arrancaram risadas genuínas com frequência. Nesse texto, quero falar das diferenças e semelhanças entre duas delas: _Arrested Development_ (2003-2005) e _Trailer Park Boys_ (2001-2007).
""")
    st.image(
        "https://miro.medium.com/v2/resize:fit:2000/0*JC8koPijskjpITS-.jpg",
        caption="Arrested Development",
        width=400
    )

    st.markdown("""
    **ARRESTED DEVELOPMENT E SUTILEZAS**

    _It's called an 'illusion', Michael. A 'trick' is what a whore does for money._

    No período pré-streaming, as séries de televisão - especialmente comédias - não eram acompanhadas pelo público com tanta linearidade. A audiência dependia do dia da semana e do horário, episódios eram assistidos fora de ordem, e era mais difícil acompanhar 100% de um programa.

    É claro que isso não era um problema para _Friends_, _Sex and the City_ e _Everybody Loves Raymond_, pois as séries eram construídas exatamente para este tipo de audiência. Qualquer episódio pode ser assistido a qualquer momento, sem efeito nenhum na efetividade do humor.

    Esse não era o caso de _Arrested Development_. As piadas são construídas ao longo dos episódios, e até das temporadas. A genialidade está, quase sempre, nas entrelinhas. Os momentos verdadeiramente hilários da série - que são MUITOS - acontecem na sutileza das relações entre os personagens.

    Uma explosão de raiva de Buster, por exemplo, não tem valor. Mas dado o contexto da sua relação de submissão com a mãe (icônica Lucille), me fez gargalhar **histericamente**. As piadas não são requintadas, mas certamente são construídas de forma sofisticada. Sua vanguarda trouxe simultaneamente dezenas de prêmios, um Emmy de Melhor Comédia e o cancelamento por falta de audiência.

    _'Se isso é um criticismo velado sobre mim, não vou validar e nem responder!'_
    """)

    st.markdown("""
    **TRAILER PARK BOYS E ATROPELAMENTOS**

    Uma câmera de baixíssima qualidade seguindo dois amigos de infância que acabaram de sair da cadeia e estão retornando à comunidade de trailers em que moram. Essa é a premissa da série _Trailer Park Boys_, que contém a diversidade de personagens mais hilária de todos os tempos.

    As pessoas que vivem nessa comunidade são quase todas caricaturadas. Rick é um brutamonte que atira em tudo que se move. Jullian quer ser empreendedor, e está sempre (**sempre.**) com um copo de whisky na mão. Bubbles é apaixonado por gatos e rouba carrinhos de supermercado para sobreviver. Lahey é o supervisor alcoólatra do parque, casado com seu auxiliar Randy (que é literalmente alérgico a camisetas).

    A mistura dessas figuras, os embates causados pelos seus exacerbados traços de personalidade e a química entre os personagens torna _Trailer Park Boys_ uma das séries mais hilárias que já tive o prazer de assistir.

    _Fuck, I missed jail this year. Was it awesome?_
    """)
    st.image(
        "https://www.indiewire.com/wp-content/uploads/2014/03/trailer-park-boys.jpg",
        caption="Julian, Bubbles e Rick",
        width=400
    )

    st.markdown("""
    Não há nuances, nem entrelinhas carregadas. São diálogos diretos e escrachados entre personagens igualmente diretos e escrachados. E de alguma forma, a série consegue ser tão espetacular quanto _Arrested Development_.

    Que belo testamento à diversidade da comédia: a narrativa sofisticada de _Arrested Development_ torna ideias bobas hilárias, enquanto a narrativa boba de _Trailer Park Boys_ produz ideias hilárias sofisticadas. São séries absolutamente geniais que ocupam os extremos de um espectro amplo e divertido que temos a sorte de poder explorar - cujo exato centro é _Community_.
    """)
st.divider()
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0;">
        <div>
            <h3><b>Sobre Baby Reindeer: O espectro da sinceridade na arte</b> </h3>
        </div>
        <div>
            <img src="https://media.glamour.com/photos/661d39dd2bf771e1378d3e83/master/w_2560%2Cc_limit/BABY%2520REINDEER%2520280324%2520Baby_Reindeer_n_S1_E2_00_20_42_07.png%2CBaby_Reindeer_n_S1_E2_00_20_42_07.jpg" 
            style="width: 400px; height: auto; margin-left: 20px;">
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
if st.button("Ler mais", key='Beberena'):
    st.markdown("""
        Um conceito interessante na arte e que afeta diretamente como percebemos uma obra, é a **sinceridade**. 
        É algo simultaneamente difícil de definir, e óbvio de identificar.

        Ser sincero não é sinônimo de ser literal - uma obra de ficção científica como _Watchmen_ ou um filme completamente abstrato 
        como _Eraserhead_ podem ser profundamente sinceros, enquanto documentários como _The Last Dance_ ou filmes biográficos como 
        _Boyhood_ podem ser cínicos e superficiais. É abstrato, mas eu, pessoalmente, consigo identificar se o que assisto 
        é sincero ou não imediatamente - mesmo que não saiba muito bem explicar o porquê.

        A maioria das séries de prestígio, são sinceras, e a maioria das séries medianas, são superficiais. 
        Há exceções para ambas as regras, e **Bebê Rena** é o outlier mais escandaloso que já vi.
    """)

    # Inserir a imagem associada ao texto
    st.image("https://www.joblo.com/wp-content/uploads/2024/07/Baby-Reindeer-lawsuit-1024x538.jpg",
             caption="Imagem de divulgação de Bebê Rena - 2024")

    # Continuação do texto
    st.markdown("""
        A história é baseada em situações de abuso reais que o criador, escritor e protagonista Richard Gadd passou, 
        e digo com segurança que nunca vi nada igual.

        A sensação é de estar assistindo a uma confissão, ou a conclusão de sessões de terapia. 
        O que inicialmente parece ser uma série visualmente sem graça e com uma narração desestimulante, se desenrola em um inesperado soco no estômago. 
        Após os primeiros episódios, há uma mudança sutil na narrativa: ela se afasta de algo um pouco mais subjetivo, e torna-se um desabafo direto. Por isso, quando Richard Gadd vai para lugares mais sombrios, sua honestidade bruta nos leva com ele.

        A história não é contada com a maestria de um bom escritor, e seu visual não chama a atenção.
        Mas o criador reflete sobre os abusos que sofreu, destrincha os seus fracassos e admite fantasias sombrias de uma forma tão crua, dolorosa e confessional que torna 
        **Bebê Rena** algo especial.
    """)
st.divider()

# ticker = st.sidebar.selectbox("Seções", tickers)


# st.title("Olá!!!")


# st.header("Orientações:")
# st.markdown("""Quero colocar o máximo de análises possível, e de alguma forma colocar a opção de recebeer novos dados dos preditores para fazer predições da variavel resposta. Se vira, amigão! Algo importante é: seria legal adicionar um recurso de salvar novos objetos durante a análise. EX: salvar os ACP numa matriz para depois fazer a MANOVA.
#   """)


