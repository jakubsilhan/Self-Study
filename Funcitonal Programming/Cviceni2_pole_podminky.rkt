;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-reader.ss" "lang")((modname Cviceni2_pole_podminky) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
; Uloha 1

; nalezt druhy prvek
(define (druhy list)
  (car (cdr list))
  )

(druhy '(1 2 3 4))

; nalezt posledni prvek
(define (posledni list)
  (car (reverse list)))

(posledni '(1 2 3 4))

; seznam bez posledniho
(define (bezkonce list)
  (reverse(cdr (reverse list))))

(bezkonce '(1 2 3 4))

; Uloha 2
; vratit seznam bez druheho prvku
(define (bezdruheho list)
  (cons (car list)
        (cdr (cdr list))
  )
)

(bezdruheho '(1 2 3 4 5))

; Uloha 3
; prohodit par - lze vice zpusoby
(define (prohod par)
  (cons (car (cdr par))
        (list (car par))
  )
)

(prohod '(1 2))

; Uloha 4
; delitelne 2 a 3
(define (mod23? num)
  (and (= 0 (modulo num 2))
       (= 0 (modulo num 3))
  )
)

(mod23? 12)
(mod23? 15)

; omezi cislo na interval
(define (omezit mini x maxi)
  (cond [(< x mini) mini]
        [(> x maxi) maxi]
        [else x]))
(omezit 0 19 20)

; Uloha 5
; otestuje sudost
(define (suda? List)
  (cond [(empty? List) #t]
        [(odd? (car List)) #f]
        [else (suda? (cdr List))]))

(suda? '(4 2 8))

; Uloha 6
; suma cisel v seznamu
(define (secti List)
  (cond [(empty? List) 0]
        [else (+ (car List) (secti (cdr List)))]
  )
)

(secti '(25 31 6 10))

; Uloha 7
; rozdeli seznam na stejne dlouhe casti
(define (rozdel List)
  (delit List '() '()))

(define (delit L L1 L2)
  (if (empty? L)
      (list (reverse L1) (reverse L2)) ; does this
      (delit (cdr L) L2 (cons (car L) L1)))) ; else does this

(rozdel '(25 31 6 10 37))