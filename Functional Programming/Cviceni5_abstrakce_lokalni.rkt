;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-reader.ss" "lang")((modname Cviceni5_abstrakce_lokalni) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
; 1) General function for connecting 2 list with further specific implementation

(define (seznamator kombi L1 L2)
  (cond [(empty? L1) L2]
        [(empty? L2) L1]
        [else (cons (kombi (car L1) (car L2)) (seznamator kombi (cdr L1) (cdr L2)))]
  )
)
; sums numbers at the same place
(define (soucet L1 L2)
  (seznamator + L1 L2))

; takes the smaller from both lists
(define (mensi L1 L2)
  (seznamator min L1 L2))

(soucet '(1 2 2 4 3) '(2 3 1 2 4))
(mensi '(1 2 2 4 3) '(2 3 1 2 4))

; 2) General search function with customizable retrieval method
; Definition of testing kontakt struct and its list
(define-struct kontakt (jmeno telefon))

(define  kontakty (list (make-kontakt "Kuba" 735331208)
                        (make-kontakt "Zdenek" 321322123)
                        (make-kontakt "Vaclav" 821891231)))

;hledej (fun X Y) Y (fun X) (list X)-> list
(define (hledej shoda? hodnota vysledek L)
    (cond [(empty? L) '()]
          [(shoda? hodnota (car L)) (vysledek (car L))]
          [else (hledej shoda? hodnota vysledek (cdr L))])
    )

;hledej_cislo X list -> 
(define (hledej_cislo hodnota L)
  (local (
          (define (stejne_cislo hodnota clovek)
            (= hodnota (kontakt-telefon clovek)))
          )
    (hledej stejne_cislo hodnota kontakt-jmeno L)))

(define (hledej_jmeno hodnota L)
  (local (
          (define (stejne_jmeno hodnota clovek)
            (equal? hodnota (kontakt-jmeno clovek))
          ))
    (hledej stejne_jmeno hodnota kontakt-telefon L)))

(hledej_cislo 735331208  kontakty)
(hledej_jmeno "Zdenek" kontakty)

; 3) Tree extraction
; Definition of testing tree
(define-struct  uzelBVS  (klic  levy  pravy))
(define testovaci
    (make-uzelBVS 20
        (make-uzelBVS 15
            (make-uzelBVS 8
                '()
                (make-uzelBVS 12
                    '() '()))
            (make-uzelBVS 17 '() '()))
        (make-uzelBVS 52
            (make-uzelBVS 39
                (make-uzelBVS 24 '() '())
                '())
            (make-uzelBVS 60 '() '()))))

; Extract numbers that conform to specified condition
(define (vyberBVS podminka? strom)
  (cond [(empty? strom) '()]
        [(podminka? (uzelBVS-klic strom))
         (append (vyberBVS podminka? (uzelBVS-levy strom)) (list(uzelBVS-klic strom)) (vyberBVS podminka? (uzelBVS-pravy strom)))]
        [else
         (append (vyberBVS podminka? (uzelBVS-levy strom)) (vyberBVS podminka? (uzelBVS-pravy strom)))]))

(vyberBVS even? testovaci)

; 4) Search BVS
(define (hledejBVS? L_podminka extrakce hodnota strom)
  (cond [(empty? strom) #f]
        [(equal? (extrakce hodnota) (uzelBVS-klic strom)) #t]
        [else (hledejBVS?
               L_podminka
               extrakce
               hodnota
               (if (L_podminka hodnota (uzelBVS-klic strom)) (uzelBVS-levy strom)
                             (uzelBVS-pravy strom)))]))

(define (hledejBVSCislo? L_podminka hodnota strom)
  (local ((define (extrakce_cislo num)
           (+ 0 num)))
    (hledejBVS? L_podminka extrakce_cislo hodnota strom)))

(hledejBVSCislo? < 20 testovaci)
(hledejBVSCislo? < 13 testovaci)