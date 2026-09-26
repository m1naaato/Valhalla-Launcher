// Priority: 800
/*
    Register Custom Creative Tab for Arcadia.
    Contains only Arcadia custom items.
    Created by vyrriox.
*/

StartupEvents.registry('creative_mode_tab', event => {
    event.create('arcadia:main')
        .displayName('Arcadia')
        .icon(() => 'arcadia:arcadia_key')
        .content(() => [
            'arcadia:basic_key',
            'arcadia:common_key',
            'arcadia:rare_key',
            'arcadia:legendary_key',
            'arcadia:arcadia_key',
            'arcadia:vote_key',
            'arcadia:token_casino',
            'arcadia:atm',
            'arcadia:music_disc_mike_le_loulou',
            'arcadia:music_disc_vyrriox_trois_femmes',
            'arcadia:music_disc_vyrriox_sac_a_gros_pt1',
            'arcadia:music_disc_vyrriox_sac_a_gros_pt2',
            'arcadia:music_disc_vyrriox_patee',
            'arcadia:music_disc_vyrriox_la_naine_pt1',
            'arcadia:music_disc_vyrriox_la_naine_pt2',
            'arcadia:music_disc_vyrriox_la_naine_pt3',
            'arcadia:music_disc_vyrriox_la_femme_de_joie',
            'arcadia:music_disc_peter_le_frein_pt1',
            'arcadia:music_disc_peter_le_frein_pt2',
            'arcadia:music_disc_peter_le_frein_pt3',
            'arcadia:music_disc_peter_le_frein_pt4',
            'arcadia:music_disc_peter_le_frein_pt5',
            'arcadia:music_disc_boit_ton_picher',
            'arcadia:music_disc_dans_la_tavern_lulu',
            'arcadia:music_disc_janette',
            'arcadia:music_disc_la_boulette_pt1',
            'arcadia:music_disc_la_boulette_pt2',
            'arcadia:music_disc_au_pactole',

            // Fusion Core Chain - Tier 0
            'arcadia:alloy_blend',
            'arcadia:diamond_matrix',
            'arcadia:infused_steel',
            'arcadia:nether_concentrate',
            'arcadia:energized_dust',
            'arcadia:wiring_bundle',

            // Fusion Core Chain - Tier 1
            'arcadia:refined_alloy_ingot',
            'arcadia:hardened_steel_compound',
            'arcadia:energized_crystal',
            'arcadia:treated_composite_plate',

            // Fusion Core Chain - Tier 2
            'arcadia:quantum_circuit',
            'arcadia:plasma_cell',
            'arcadia:reinforced_casing',
            'arcadia:thermal_conductor',

            // Fusion Core Chain - Tier 3
            'arcadia:fusion_matrix',
            'arcadia:containment_field_generator',
            'arcadia:neutron_reflector',

            // Fusion Core - Final
            'arcadia:fusion_core',

            // Special
            'arcadia:heart_of_arcadia',

            // Adept Armor + Items
            'arcadia:adept_helmet',
            'arcadia:adept_chestplate',
            'arcadia:adept_leggings',
            'arcadia:adept_boots',
            'arcadia:adept_grimoire',
            'arcadia:adept_pendant',
            'arcadia:adept_candle',
            'arcadia:adept_incense',
            'arcadia:adept_staff',
            'arcadia:adept_seal',
            'arcadia:adept_chalice',
            'arcadia:adept_orb',
            'arcadia:adept_scroll',
            'arcadia:adept_relic',

            // Heretic Armor + Items
            'arcadia:heretic_helmet',
            'arcadia:heretic_chestplate',
            'arcadia:heretic_leggings',
            'arcadia:heretic_boots',
            'arcadia:heretic_tome',
            'arcadia:heretic_blood_vial',
            'arcadia:heretic_dagger',
            'arcadia:heretic_chain',
            'arcadia:heretic_skull_totem',
            'arcadia:heretic_icon',
            'arcadia:heretic_crystal',
            'arcadia:heretic_bone_charm',
            'arcadia:heretic_poison_flask',
            'arcadia:heretic_mark'
        ]);
});
