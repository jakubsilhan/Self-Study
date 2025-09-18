;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-reader.ss" "lang")((modname Cviceni3_struktury) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(define-struct zbozi (nazev cena kusu))
(define sklad
  (list (make-zbozi "Chleba" 30 10)
        (make-zbozi "Mleko" 20 15)
        (make-zbozi "Zelenina" 15 20)
        (make-zbozi "Cola" 30 10)))

(zbozi-nazev (car sklad))

; 2) Najdi cenu pro zbozi
(define (najdi-cenu jmeno seznam)
  (cond [(empty? seznam) 0]
        [(string=? jmeno (zbozi-nazev (car seznam))) (zbozi-cena (car seznam))] ; string=? pro porovnavani retezcu
        [else (najdi-cenu jmeno (cdr seznam))]
  )
)

(define (najdi-cenu2 j s) ; pristup bottom up
  (cond [(empty? s) 0]
        [(equal? j (zbozi-nazev (car s))) (zbozi-cena (car s))]
        [else (najdi-cenu2 j (cdr s))]
        ))

(najdi-cenu "Zelenina" sklad)
(najdi-cenu2 "Zelenina" sklad)

; 3) Celkova cena skladu
(define (celkova-hodnota seznam) ; pristup bottom up
  (cond [(empty? seznam) 0]
        [else (+ (* (zbozi-cena (car seznam)) (zbozi-kusu (car seznam))) (celkova-hodnota (cdr seznam)))]))

(define (celkova-hodnota2 seznam)
  (scitej-ceny 0 seznam))

(define (scitej-ceny suma seznam) ; pristup top to bottom 
  (cond [(empty? seznam) suma]
        [else (scitej-ceny (+ suma (* (zbozi-cena (car seznam)) (zbozi-kusu (car seznam)))) (cdr seznam))]))



(celkova-hodnota sklad)
(celkova-hodnota2 sklad)

; 4) Cena objednavky
(define-struct objednavka (nazev kusu))

(define (cena-objednavky objednavka sklad)
  (cena-objednavky-sub 0 objednavka sklad))

(define (cena-objednavky-sub suma objednavky sklad)
  (cond [(empty? objednavky) suma]
        [else (cena-objednavky-sub
               (+ suma
                  (* (objednavka-kusu (car objednavky))
                     (najdi-cenu (objednavka-nazev (car objednavky))
                                 sklad)))
               (cdr objednavky)
               sklad)]))

(cena-objednavky (list (make-objednavka "Chleba" 5)
                       (make-objednavka "Mleko" 3))
                 sklad)

; 5) Odebrani kusu
(define (vydej sklad nazev kusu)
  (cond [(empty? sklad) sklad]
        [(equal? nazev (zbozi-nazev (car sklad)))
         (cons (make-zbozi nazev (zbozi-cena (car sklad)) (- (zbozi-kusu (car sklad)) kusu)) (cdr sklad)) ; pridat odebrani pokud nula
        ]
        [else (cons (car sklad) (vydej (cdr sklad) nazev kusu))]))

(vydej sklad "Mleko" 15) 