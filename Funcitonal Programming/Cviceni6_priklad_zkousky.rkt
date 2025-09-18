;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-reader.ss" "lang")((modname Cviceni6_priklad_zkousky) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
; 1) Vzorec
; f: number number -> number
; Calculates a formula
(define (f a b)
  (/
   (+ (/ a b) (/ b a))
   (* a b)
  )
)

(f 1 2)

; 2) Vyber ze seznamu
; vyber: number list -> number
; Finds the number at n index of the list L
(define (vyber n L)
  (cond [(empty? L) '()]
        [(= 1 n) (car L)]
        [else (vyber (- n 1) (cdr L))]
  )
)

(list-ref '(10 20 30 40 50) 2)

(member 10 '(10 20 30 40 50))


(vyber 3 '(10 20 30 40 50))

; 3) Struktura
(define-struct oddeleni (nazev zamestnanci))

(define podnik (list
(make-oddeleni "Prodej"
'("Anna Bílá" "Lída Žlutá" "Petr Modrý"))
(make-oddeleni "Vývoj"
'("Josef Zelený" "Lenka Růžová" "Alena Černá"))
))

; hledej-oddeleni: string (list oddeleni) -> string
; Finds the department from list of departments, which contains the searched name
(define (hledej-oddeleni jmeno seznam-oddeleni)
  (cond [(empty? seznam-oddeleni) '()]
        [(projdi-oddeleni? jmeno (oddeleni-zamestnanci (car seznam-oddeleni))) (oddeleni-nazev (car seznam-oddeleni))]
        [else (hledej-oddeleni jmeno (cdr seznam-oddeleni))]
  )
)

; projdi-oddeleni?: string (list string) -> boolean
; Checks if a name is contained in the list
(define (projdi-oddeleni? jmeno zamestnanci)
  (cond [(empty? zamestnanci) #f]
        [(equal? jmeno (car zamestnanci)) #t]
        [else (projdi-oddeleni? jmeno (cdr zamestnanci))]
  )
)

; Druhou funkci lze nahradit funkci member, ale do zkousky chce nase vlastni

(hledej-oddeleni "Petr Modrý" podnik)
(hledej-oddeleni "Lenka Zelená" podnik)
(hledej-oddeleni "Lenka Růžová" podnik)