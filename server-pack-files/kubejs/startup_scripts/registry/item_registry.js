// Priority: 900
/*
    Registering Custom Items for Arcadia V2.
    Optimized for KubeJS 1.21.1 (NeoForge).
    Created by vyrriox.
*/

StartupEvents.registry('item', event => {
    // Keys & Utility
    event.create('arcadia:basic_key').texture('arcadia:item/basic_key');
    event.create('arcadia:common_key').texture('arcadia:item/common_key');
    event.create('arcadia:rare_key').texture('arcadia:item/rare_key');
    event.create('arcadia:legendary_key').texture('arcadia:item/legendary_key');
    event.create('arcadia:arcadia_key').rarity('epic').glow(true).texture('arcadia:item/arcadia_key');
    event.create('arcadia:vote_key').texture('arcadia:item/vote_key');
    event.create('arcadia:token_casino').texture('arcadia:item/token_casino');

    // Music Discs (20 tracks)
    const discs = [
        'mike_le_loulou', 'vyrriox_trois_femmes', 'vyrriox_sac_a_gros_pt1', 'vyrriox_sac_a_gros_pt2',
        'vyrriox_patee', 'vyrriox_la_naine_pt1', 'vyrriox_la_naine_pt2', 'vyrriox_la_naine_pt3',
        'vyrriox_la_femme_de_joie', 'peter_le_frein_pt1', 'peter_le_frein_pt2', 'peter_le_frein_pt3',
        'peter_le_frein_pt4', 'peter_le_frein_pt5', 'boit_ton_picher', 'dans_la_tavern_lulu',
        'janette', 'la_boulette_pt1', 'la_boulette_pt2', 'au_pactole'
    ];

    discs.forEach(id => {
        event.create(`arcadia:music_disc_${id}`)
            .displayName('Music Disc')
            .jukeboxPlayable(`arcadia:${id}`)
            .texture(`arcadia:item/music_disc_${id}`)
            .rarity('rare')
            .maxStackSize(1);
    });

    // Transitional Items for Sequenced Assembly
    event.create('arcadia:incomplete_netherite_block')
        .texture('minecraft:item/netherite_scrap')
        .displayName('Incomplete Netherite Block');

    // ===== FUSION CORE CRAFTING CHAIN =====

    // Tier 0 - Processed Materials
    event.create('arcadia:alloy_blend')
        .displayName('Alloy Blend')
        .texture('arcadia:item/alloy_blend')
        .rarity('common');

    event.create('arcadia:diamond_matrix')
        .displayName('Compressed Diamond Matrix')
        .texture('arcadia:item/diamond_matrix')
        .rarity('uncommon')
        .glow(true);

    event.create('arcadia:infused_steel')
        .displayName('Infused Steel Bar')
        .texture('arcadia:item/infused_steel')
        .rarity('common');

    event.create('arcadia:nether_concentrate')
        .displayName('Nether Concentrate')
        .texture('arcadia:item/nether_concentrate')
        .rarity('uncommon')
        .glow(true);

    event.create('arcadia:energized_dust')
        .displayName('Energized Dust')
        .texture('arcadia:item/energized_dust')
        .rarity('common');

    event.create('arcadia:wiring_bundle')
        .displayName('Wiring Bundle')
        .texture('arcadia:item/wiring_bundle')
        .rarity('common');

    // Tier 1 - Refined Components
    event.create('arcadia:refined_alloy_ingot')
        .displayName('Refined Alloy Ingot')
        .texture('arcadia:item/refined_alloy_ingot')
        .rarity('uncommon');

    event.create('arcadia:hardened_steel_compound')
        .displayName('Hardened Steel Compound')
        .texture('arcadia:item/hardened_steel_compound')
        .rarity('uncommon');

    event.create('arcadia:energized_crystal')
        .displayName('Energized Crystal')
        .texture('arcadia:item/energized_crystal')
        .rarity('uncommon')
        .glow(true);

    event.create('arcadia:treated_composite_plate')
        .displayName('Treated Composite Plate')
        .texture('arcadia:item/treated_composite_plate')
        .rarity('uncommon');

    // Tier 2 - Advanced Components
    event.create('arcadia:quantum_circuit')
        .displayName('Quantum Circuit')
        .texture('arcadia:item/quantum_circuit')
        .rarity('rare');

    event.create('arcadia:plasma_cell')
        .displayName('Plasma Cell')
        .texture('arcadia:item/plasma_cell')
        .rarity('rare')
        .glow(true);

    event.create('arcadia:reinforced_casing')
        .displayName('Reinforced Casing')
        .texture('arcadia:item/reinforced_casing')
        .rarity('rare');

    event.create('arcadia:thermal_conductor')
        .displayName('Thermal Conductor')
        .texture('arcadia:item/thermal_conductor')
        .rarity('rare');

    // Tier 2 - Transitional items for sequenced assembly
    event.create('arcadia:incomplete_plasma_cell')
        .displayName('Incomplete Plasma Cell')
        .texture('arcadia:item/incomplete_plasma_cell');

    event.create('arcadia:incomplete_reinforced_casing')
        .displayName('Incomplete Reinforced Casing')
        .texture('arcadia:item/incomplete_reinforced_casing');

    // Tier 3 - Elite Components
    event.create('arcadia:fusion_matrix')
        .displayName('Fusion Matrix')
        .texture('arcadia:item/fusion_matrix')
        .rarity('epic')
        .glow(true);

    event.create('arcadia:containment_field_generator')
        .displayName('Containment Field Generator')
        .texture('arcadia:item/containment_field_generator')
        .rarity('epic')
        .glow(true);

    event.create('arcadia:neutron_reflector')
        .displayName('Neutron Reflector')
        .texture('arcadia:item/neutron_reflector')
        .rarity('epic');

    event.create('arcadia:incomplete_neutron_reflector')
        .displayName('Incomplete Neutron Reflector')
        .texture('arcadia:item/incomplete_neutron_reflector');

    // FINAL - Fusion Core
    event.create('arcadia:fusion_core')
        .displayName('Fusion Core')
        .texture('arcadia:item/fusion_core')
        .rarity('epic')
        .glow(true)
        .maxStackSize(1);

    // ===== CROSS-MOD BRIDGE COMPONENTS =====
    // Bridge items that unify multiple mods (Create, TFMG, Mekanism, Ars Nouveau, Occultism, IE, Apotheosis).
    // Used as gate ingredients for hardened mid/late-game recipes.

    // MEDIUM bridge: Create + TFMG + Mekanism + Ars Nouveau
    event.create('arcadia:arcane_circuit')
        .displayName('Arcane Circuit')
        .texture('arcadia:item/arcane_circuit')
        .rarity('uncommon')
        .glow(true);

    // HARD bridge: Ars Nouveau + Mekanism + Occultism + Create
    event.create('arcadia:ethereal_alloy')
        .displayName('Ethereal Alloy')
        .texture('arcadia:item/ethereal_alloy')
        .rarity('rare')
        .glow(true);

    // HARD bridge: Create + TFMG + Mekanism + Immersive Engineering
    event.create('arcadia:industrial_heart')
        .displayName('Industrial Heart')
        .texture('arcadia:item/industrial_heart')
        .rarity('rare')
        .glow(true);

    // ENDGAME bridge: Ars Nouveau + Occultism + Create + Apotheosis
    event.create('arcadia:rune_matrix')
        .displayName('Rune Matrix')
        .texture('arcadia:item/rune_matrix')
        .rarity('epic')
        .glow(true);

    // Transitional item for Industrial Heart sequenced assembly
    event.create('arcadia:incomplete_industrial_heart')
        .displayName('Incomplete Industrial Heart')
        .texture('arcadia:item/industrial_heart');

    // ===== COEUR D'ARCADIA =====
    event.create('arcadia:heart_of_arcadia')
        .displayName('Heart of Arcadia')
        .texture('arcadia:item/heart_of_arcadia')
        .rarity('epic')
        .glow(true)
        .maxStackSize(1);

    // ===== ADEPT ARMOR SET =====
    event.create('arcadia:adept_helmet', 'helmet')
        .material('arcadia:adept')
        .texture('arcadia:item/adept_helmet')
        .rarity('uncommon');

    event.create('arcadia:adept_chestplate', 'chestplate')
        .material('arcadia:adept')
        .texture('arcadia:item/adept_chestplate')
        .rarity('uncommon');

    event.create('arcadia:adept_leggings', 'leggings')
        .material('arcadia:adept')
        .texture('arcadia:item/adept_leggings')
        .rarity('uncommon');

    event.create('arcadia:adept_boots', 'boots')
        .material('arcadia:adept')
        .texture('arcadia:item/adept_boots')
        .rarity('uncommon');

    // ===== HERETIC ARMOR SET =====
    event.create('arcadia:heretic_helmet', 'helmet')
        .material('arcadia:heretic')
        .texture('arcadia:item/heretic_helmet')
        .rarity('uncommon');

    event.create('arcadia:heretic_chestplate', 'chestplate')
        .material('arcadia:heretic')
        .texture('arcadia:item/heretic_chestplate')
        .rarity('uncommon');

    event.create('arcadia:heretic_leggings', 'leggings')
        .material('arcadia:heretic')
        .texture('arcadia:item/heretic_leggings')
        .rarity('uncommon');

    event.create('arcadia:heretic_boots', 'boots')
        .material('arcadia:heretic')
        .texture('arcadia:item/heretic_boots')
        .rarity('uncommon');

    // ===== ADEPT UNIQUE ITEMS (10) =====
    event.create('arcadia:adept_grimoire')
        .texture('arcadia:item/adept_grimoire').rarity('rare').maxStackSize(1);
    event.create('arcadia:adept_pendant')
        .texture('arcadia:item/adept_pendant').rarity('uncommon').maxStackSize(1);
    event.create('arcadia:adept_candle')
        .texture('arcadia:item/adept_candle').rarity('common');
    event.create('arcadia:adept_incense')
        .texture('arcadia:item/adept_incense').rarity('common');
    event.create('arcadia:adept_staff')
        .texture('arcadia:item/adept_staff').rarity('rare').maxStackSize(1);
    event.create('arcadia:adept_seal')
        .texture('arcadia:item/adept_seal').rarity('uncommon').maxStackSize(1);
    event.create('arcadia:adept_chalice')
        .texture('arcadia:item/adept_chalice').rarity('uncommon').maxStackSize(1);
    event.create('arcadia:adept_orb')
        .texture('arcadia:item/adept_orb').rarity('rare').glow(true).maxStackSize(1);
    event.create('arcadia:adept_scroll')
        .texture('arcadia:item/adept_scroll').rarity('uncommon');
    event.create('arcadia:adept_relic')
        .texture('arcadia:item/adept_relic').rarity('epic').glow(true).maxStackSize(1);

    // ===== HERETIC UNIQUE ITEMS (10) =====
    event.create('arcadia:heretic_tome')
        .texture('arcadia:item/heretic_tome').rarity('rare').maxStackSize(1);
    event.create('arcadia:heretic_blood_vial')
        .texture('arcadia:item/heretic_blood_vial').rarity('uncommon');
    event.create('arcadia:heretic_dagger')
        .texture('arcadia:item/heretic_dagger').rarity('rare').maxStackSize(1);
    event.create('arcadia:heretic_chain')
        .texture('arcadia:item/heretic_chain').rarity('uncommon').maxStackSize(1);
    event.create('arcadia:heretic_skull_totem')
        .texture('arcadia:item/heretic_skull_totem').rarity('rare').maxStackSize(1);
    event.create('arcadia:heretic_icon')
        .texture('arcadia:item/heretic_icon').rarity('uncommon').maxStackSize(1);
    event.create('arcadia:heretic_crystal')
        .texture('arcadia:item/heretic_crystal').rarity('rare').glow(true).maxStackSize(1);
    event.create('arcadia:heretic_bone_charm')
        .texture('arcadia:item/heretic_bone_charm').rarity('uncommon').maxStackSize(1);
    event.create('arcadia:heretic_poison_flask')
        .texture('arcadia:item/heretic_poison_flask').rarity('uncommon');
    event.create('arcadia:heretic_mark')
        .texture('arcadia:item/heretic_mark').rarity('epic').glow(true).maxStackSize(1);
});
