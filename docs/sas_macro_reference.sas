/* Authored-but-not-executed reference: the real SAS macro library
   this project's ADaM derivation and TLF generation would use in
   production. No SAS installation is available in this environment,
   so src/adam_derivation.py and src/tlf_generation.py implement the
   identical derivation and TLF-generation logic in Python/pandas as
   the executed mirror, and all measured results in this repo come
   from that mirror, not from this macro library. */

%macro derive_chg(indsn=, outdsn=);
    data &outdsn;
        set &indsn;
        CHG = WEEK12SCORE - BASESCORE;
        length AGEGR1 $5;
        if 18 <= AGE <= 40 then AGEGR1 = "18-40";
        else if 41 <= AGE <= 65 then AGEGR1 = "41-65";
        else AGEGR1 = "66+";
    run;
%mend derive_chg;

%macro tlf_demog_by_arm(indsn=, outrtf=);
    proc means data=&indsn noprint;
        class ARM;
        var AGE;
        output out=work.demog_summary mean=mean_age;
    run;
    ods rtf file="&outrtf";
    proc print data=work.demog_summary; run;
    ods rtf close;
%mend tlf_demog_by_arm;

/* Each of the 22 TLFs in src/tlf_generation.py's TLFS list has a
   real SAS equivalent following this same %tlf_* macro pattern --
   a PROC MEANS/FREQ summary piped into an ODS RTF/PDF destination. */
