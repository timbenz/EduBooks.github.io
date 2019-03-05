//package hand;


import java.util.*;

/**
 * Created by AlexNewman on 2/12/17.
 */
class CardSelection {
    private ArrayList handi;
    private float[] score;
    private List<String> cuts;
    private ArrayList<String> cutcombos;
    private String[][] subsets;

    private CardSelection(String[] input) {
        this.handi = new ArrayList(Arrays.asList(input));
        this.cuts = new ArrayList<>(); //Don't use this after you get cutcombos
        this.cutcombos = new ArrayList<>();
        this.subsets = new String[15][4];
        this.score = new float[15];

        String[] suit = {"D", "S", "C", "H"};

        for (String v : suit) {
            for (int num = 2; num < 11; num++) {
                cuts.add(num + v);
            }
            cuts.add("A" + v);
            cuts.add("J" + v);
            cuts.add("Q" + v);
            cuts.add("K" + v);
        }
        cutcard(this);
        combinations(this);
    }


    private static void cutcard(CardSelection cards) {
        for (String s : cards.cuts) {
            if (!cards.handi.contains(s)) {
                cards.cutcombos.add(s); //creates list of potential cut cards
            }
        }
    }

    /* Finds all combos of hands and puts them in array called subset*/
    private static void combinations(CardSelection hands) {
        Object[] objs = hands.handi.toArray();
        String[] handi = new String[6];
        for (int i = 0; i < handi.length; i++) {
            String someString = (String) objs[i];
            handi[i] = someString;
        }
        String[][] newhand = {
                {handi[0], handi[1], handi[2], handi[3]},
                {handi[0], handi[1], handi[2], handi[4]},
                {handi[0], handi[1], handi[2], handi[5]},
                {handi[0], handi[1], handi[3], handi[4]},
                {handi[0], handi[1], handi[3], handi[5]},
                {handi[0], handi[1], handi[4], handi[5]},
                {handi[0], handi[2], handi[3], handi[4]},
                {handi[0], handi[2], handi[3], handi[5]},
                {handi[0], handi[2], handi[4], handi[5]},
                {handi[0], handi[3], handi[4], handi[5]},
                {handi[1], handi[2], handi[3], handi[4]},
                {handi[1], handi[2], handi[3], handi[5]},
                {handi[1], handi[2], handi[4], handi[5]},
                {handi[1], handi[3], handi[4], handi[5]},
                {handi[2], handi[3], handi[4], handi[5]}};
        hands.subsets = newhand;

    }

    private void flush() {
        for (int i = 0; i < subsets.length; i++) { //For every combo
            String[] combo = subsets[i]; //Get combo
            char firstsuit = combo[0].charAt(1); //Get first suit; eg. D H C S
            String firstsuitstring = Character.toString(firstsuit);
            int numsame = 0;
            for (String y : combo) {
                if (y.contains(firstsuitstring)) {
                    numsame++;
                }
            }
            /* If all cards in hand are same suit */
            if (numsame == 4) {
                int x = 0;
                /* Adds potential for cut card matching suit*/
                for (String s : cutcombos) {
                    String[] val = s.split("");
                    if (val[1].equals(firstsuitstring)) {
                        x += 1;
                    }
                }
                double y = 1.00 * x / 46;
                score[i] += 4 + y;
            }
        }
    }


    private int fifteensplit(String card) {

        String[] valarray = card.split("");
        if (valarray[0].equals("K") || valarray[0].equals("Q") || valarray[0].equals("J") || valarray.length == 3) {
            return 10;
        } else if (valarray[0].equals("A")) {
            return 1;
        } else {
            return Integer.parseInt(valarray[0]);
        }
    }

    private float fifteenchecker(ArrayList<Integer> nums) {
        ArrayList<Integer> vals = new ArrayList<>();
        for (int ind : nums) {
            vals.add(ind);
        }
        float fifteentotal = (float) 0.00;

        if (nums.get(0) + nums.get(1) + nums.get(2) + nums.get(3) + nums.get(4) == 15) {
            return 2;
        }

        for (int s = 0; s < nums.size(); s++) {
            for (int t = s + 1; t < nums.size(); t++) {
                for (int u = t + 1; u < nums.size(); u++) {
                    for (int v = u + 1; v < nums.size(); v++) {
                        if (nums.get(s) + nums.get(t) + nums.get(u) + nums.get(v) == 15) {
                            fifteentotal += 2;
                        }
                    }
                    if (nums.get(s) + nums.get(t) + nums.get(u) == 15) {
                        fifteentotal += 2;
                    }
                }
                if (nums.get(s) + nums.get(t) == 15) {
                    fifteentotal += 2;
                }
            }
        }
        return fifteentotal;
    }

    private void fifteen() {
        for (int i = 0; i < subsets.length; i++) { // for all potential 4-card hands
            String[] j = subsets[i]; //Get cards

            ArrayList<Integer> nums = new ArrayList<>();
            /* Converts Face/ace cards to correct numeric values*/
            for (String z : j) {
                nums.add(fifteensplit(z));
            }

            /* Takes into account cut card */
            for (String x : cutcombos) {
                float total = (float) 0.00;
                /* Same conversion for cut card */
                int val = fifteensplit(x);
                nums.add(val);
                total += fifteenchecker(nums);
                score[i] += total / 46;
                nums.remove((Object) val);
            }
        }
    }
    
    private String pairsplit(String card) {
        String[] valarray = card.split("");
        return valarray[0];
    }

    private float pairchecker(ArrayList<String> nums) {

        ArrayList<String> vals = new ArrayList<>();
        for (String ind : nums) {
            vals.add(ind);
        }
        float pairtotal = (float) 0.00;
        for (int s = 0; s < vals.size(); s++) {
            String x = vals.get(s);
            for (int t = s + 1; t < vals.size(); t++) {
                String y = vals.get(t);
                if (vals.get(s).equals(vals.get(t))) {
                    pairtotal += 2;
                    for (int u = t + 1; u < vals.size(); u++) {
                        String z = vals.get(u);
                        if (vals.get(s).equals(vals.get(u))) {
                            pairtotal += 4;
                            for (int v = u + 1; v < vals.size(); v++) {
                                if (vals.get(s).equals(vals.get(v))) {
                                    return 12; //No other pairs can exist if 4 of a kind
                                }
                            }
                            vals.remove(z);
                            break;
                        }
                    }
                    vals.remove(x);
                    vals.remove(y);
                    if (vals.size() == 3) {
                        if (vals.get(0).equals(vals.get(1)) || vals.get(0).equals(vals.get(2)) || vals.get(1).equals(vals.get(2))) {
                            pairtotal += 2;
                            if (vals.get(2).equals(vals.get(1)) && vals.get(2).equals(vals.get(0))) {
                                pairtotal += 1;
                            }

                        }
                    } else if (vals.size() == 2) {
                        if (vals.get(0).equals(vals.get(1))) {
                            pairtotal += 2;
                        }
                    }
                    return pairtotal;
                }
            }
        }
        return pairtotal;
    }

    private void pairs() {
        for (int i = 0; i < subsets.length; i++) { // for all potential 4-card hands
            String[] j = subsets[i]; //Get cards
            ArrayList<String> values = new ArrayList<>();

            for (String z : j) {
                values.add(pairsplit(z));
            }
            for (String x : cutcombos) { //Adds cut card
                float total = (float) 0.00;
                /* Same conversion for cut card */
                String val = pairsplit(x);
                values.add(val);
                total += pairchecker(values);
                score[i] += total / 46;
                values.remove(val);

            }
        }
    }

    private int runsplit(String card) {

        String[] valarray = card.split("");
        if (valarray.length == 3) {
            return 10;
        } else if (valarray[0].equals("J")) {
            return 11;
        } else if (valarray[0].equals("Q")) {
            return 12;
        } else if (valarray[0].equals("K")) {
            return 13;
        } else if (valarray[0].equals("A")) {
            return 1;
        } else {
            return Integer.parseInt(valarray[0]);
        }
    }

    private float runchecker(ArrayList<Integer> nums) {
        /* Not finished; still need to account for order*/
        ArrayList<Integer> vals = new ArrayList<>();
        for (int ind : nums) {
            vals.add(ind);
        }
        float runtotal = (float) 0.00;
        ArrayList straight = new ArrayList();
        for (int r = 0; r < vals.size(); r++) {
            int a = vals.get(r);
            for (int s = 0; s < vals.size(); s++) {
                if (r != s) {
                    int b = vals.get(s);
                    int lowest = a;
                    int highest = b;
                    if (a > b) {
                        lowest = b;
                        highest = a;
                    }
                    for (int t = 0; t < vals.size(); t++) {
                        if (t != r && t != s) {
                            int c = vals.get(t);
                            if ((lowest - 1 == c || highest + 1 == c) && highest - lowest == 1) {
                                if (c < lowest) {
                                    lowest = c;
                                } else if (c > highest) {
                                    highest = c;
                                }
                                straight.add(a);
                                straight.add(b);
                                straight.add(c);
                                runtotal += 3;
                                int prev = 0;
                                for (int v = 0; v < vals.size(); v++) {
                                    if (v != t && v != r && v != s) {
                                        int d = vals.get(v);
                                        if (lowest - 1 == d || highest + 1 == d) {
                                            straight.add(d);
                                            if (d < lowest) {
                                                lowest = d;
                                            } else {
                                                highest = d;
                                            }
                                            runtotal += 1;
                                            for (int u = 0; u < vals.size(); u++) {
                                                if (u != t && u != r && u != s && u != v) {
                                                    if ((lowest - 1 == vals.get(u) || highest + 1 == vals.get(u))) {
                                                        runtotal = 5;
                                                        return runtotal;
                                                    }
                                                    if (straight.contains(vals.get(u))) {
                                                        runtotal += 4;
                                                    }
                                                    if (d == lowest) {
                                                        lowest++;
                                                    } else if (d == highest) {
                                                        highest--;
                                                    }
                                                    return runtotal;
                                                }
                                            }
                                        } else if (straight.contains(d)) {   //This is in the right place
                                            runtotal += 3;
                                            if (d != prev && prev != 0) {
                                                runtotal += 3;
                                            }
                                            prev = d;
                                        }
                                    }
                                }
                                if (c == highest) {
                                    highest--;
                                } else if (c == lowest) {
                                    lowest++;
                                }
                                return runtotal;
                            }
                        }
                    }
                }
            }
        }
        return runtotal;
    }

    private void runs() {
        for (int i = 0; i < subsets.length; i++) { // for all potential 4-card hands
            String[] j = subsets[i]; //Get cards

            ArrayList<Integer> nums = new ArrayList<>();
            /* Converts Face/ace cards to correct numeric values*/
            for (String z : j) {
                nums.add(runsplit(z));
            }

            /* Takes into account cut card */
            for (String x : cutcombos) {
                float total = (float) 0.00;
                /* Same conversion for cut card */
                int val = runsplit(x);
                nums.add(val);
                total += runchecker(nums);
                score[i] += total / 46;

                /** Note: without casting, Java removes corresponding index*/
                nums.remove((Object) val);
            }
        }
    }

    private float nobchecker(ArrayList<Integer> vals, String l) {
        float nobs =(float) 0.00;
     for (String x : cutcombos) {
        for ( int y : vals) {
            if (x.charAt(1) == l.charAt(y))
                 nobs += 1;
        }
        }
        return nobs;
    }

    private void nobs() {
        for (int i = 0; i < subsets.length; i++) {
             String[] j = subsets[i]; //Get cards
             String l = new String();
            boolean contains = false;
             ArrayList<Integer> vals = new ArrayList<>();
             for (String k : j){
                 l += k;
                 if (k.contains("J")) {
                     contains = true;
                     vals.add(l.indexOf(k) + 1);
                 }
             }
             float total = (float) 0.00;
             if (contains) {
                 total += 1 + nobchecker(vals, l);
             }
             total = total / 46;
             score[i] += total;

        }
    }

    private void findscore() {
        int maxIndex = 0;
        for (int i = 1; i < score.length; i++) {
            int newnumber = i;
            String[] testarray = subsets[i];
            float testnum = score[newnumber];
            if (score[newnumber] > score[maxIndex]) {
                maxIndex = i;
            }
        }

        StringBuilder builder = new StringBuilder();

        for (String x : subsets[maxIndex]) {
            if (builder.length() != 0) {
                builder.append(", ");
            }
            builder.append(x);
        }
        System.out.print(builder);
        System.out.println();
    }


    public static void main(String[] args) {
        //long startTime = System.currentTimeMillis();
        String[] x = {"3H", "4S", "6D", "9H", "9S", "JD"};
        CardSelection init = new CardSelection(x);
        //TODO: Make this faster by doing for loop here instead of in each function
        init.flush();
        init.fifteen(); 
        init.pairs();
        init.runs();
        init.nobs();
        init.findscore();
        //long endTime = System.currentTimeMillis();
        //long totalTime = endTime - startTime;
        //System.out.println(totalTime);
    }

}
