// Priority: 1000
/*
    Register Custom Sound Events for Music Discs.
    Standardized for Arcadia V2.
    Created by vyrriox.
*/

StartupEvents.registry('sound_event', event => {
    const sounds = [
        'mike_le_loulou', 'vyrriox_trois_femmes', 'vyrriox_sac_a_gros_pt1', 'vyrriox_sac_a_gros_pt2',
        'vyrriox_le_bouffeur_de_patee', 'vyrriox_la_naine_pt1', 'vyrriox_la_naine_pt2', 'vyrriox_la_naine_pt3',
        'vyrriox_la_femme_de_joie', 'peter_le_frein_pt1', 'peter_le_frein_pt2', 'peter_le_frein_pt3',
        'peter_le_frein_pt4', 'peter_le_frein_pt5', 'boit_ton_picher', 'dans_la_tavern_lulu',
        'janette', 'la_boulette_pt1', 'la_boulette_pt2', 'au_pactole'
    ];

    sounds.forEach(id => {
        event.create(`arcadia:music.${id}`);
    });
});
