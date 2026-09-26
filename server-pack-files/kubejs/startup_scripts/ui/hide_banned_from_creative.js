// Priority: -500

/*
    Script to remove banned items from Creative Tabs.
    Created by vyrriox for Arcadia V2.
*/

StartupEvents.modifyCreativeTab("minecraft:search", (event) => {
    const hiddenItems = [
        // Biomes O' Plenty
        "biomesoplenty:anomaly",
        "biomesoplenty:unmapped_end_stone",
        "biomesoplenty:null_block",
        "biomesoplenty:null_leaves",
        "biomesoplenty:null_plant",
        "biomesoplenty:liquid_null_bucket",

        // Design n' Decor — IDs that actually exist in the installed version
        "dndecor:andesite_cross_bolt",
        "dndecor:andesite_dash_bolt",
        "dndecor:andesite_dot_bolt",
        "dndecor:andesite_flat_bolt",
        "dndecor:brass_cross_bolt",
        "dndecor:brass_dash_bolt",
        "dndecor:brass_dot_bolt",
        "dndecor:brass_flat_bolt",
        "dndecor:copper_cross_bolt",
        "dndecor:copper_dash_bolt",
        "dndecor:copper_dot_bolt",
        "dndecor:copper_flat_bolt",
        "dndecor:gold_cross_bolt",
        "dndecor:gold_dash_bolt",
        "dndecor:gold_dot_bolt",
        "dndecor:gold_flat_bolt",
        "dndecor:industrial_cross_bolt",
        "dndecor:industrial_dash_bolt",
        "dndecor:industrial_dot_bolt",
        "dndecor:industrial_flat_bolt",
        "dndecor:iron_cross_bolt",
        "dndecor:iron_dash_bolt",
        "dndecor:iron_dot_bolt",
        "dndecor:iron_flat_bolt",
        "dndecor:netherite_cross_bolt",
        "dndecor:netherite_dash_bolt",
        "dndecor:netherite_dot_bolt",
        "dndecor:netherite_flat_bolt",
        "dndecor:zinc_cross_bolt",
        "dndecor:zinc_dash_bolt",
        "dndecor:zinc_dot_bolt",
        "dndecor:zinc_flat_bolt",

        // Mekanism
        "mekanism:atomic_disassembler",
        "mekanism:scuba_mask",
        "mekanism:scuba_tank",
        "mekanism:free_runners",
        "mekanism:free_runners_armored",
        "mekanism:jetpack",
        "mekanism:jetpack_armored",
        "mekanism:mekasuit_helmet",
        "mekanism:mekasuit_bodyarmor",
        "mekanism:mekasuit_pants",
        "mekanism:mekasuit_boots",
        "mekanism:flamethrower",
        "mekanism:electric_bow",
        "mekanism:module_color_modulation_unit",
        "mekanism:module_laser_dissipation_unit",
        "mekanism:module_radiation_shielding_unit",
        "mekanism:module_electrolytic_breathing_unit",
        "mekanism:module_inhalation_purification_unit",
        "mekanism:module_vision_enhancement_unit",
        "mekanism:module_nutritional_injection_unit",
        "mekanism:module_dosimeter_unit",
        "mekanism:module_geiger_unit",
        "mekanism:module_jetpack_unit",
        "mekanism:module_charge_distribution_unit",
        "mekanism:module_gravitational_modulating_unit",
        "mekanism:module_elytra_unit",
        "mekanism:module_locomotive_boosting_unit",
        "mekanism:module_gyroscopic_stabilization_unit",
        "mekanism:module_hydrostatic_repulsor_unit",
        "mekanism:module_motorized_servo_unit",
        "mekanism:module_hydraulic_propulsion_unit",
        "mekanism:module_magnetic_attraction_unit",
        "mekanism:module_frost_walker_unit",
        "mekanism:module_soul_surfer_unit",
        "mekanismgenerators:module_geothermal_generator_unit",
        "mekanismgenerators:module_solar_recharging_unit",
        "mekanism:module_teleportation_unit",
        "mekanism:module_vein_mining_unit",
        "mekanism:module_blasting_unit",
        "mekanism:module_energy_unit",
        "mekanism:module_excavation_escalation_unit",
        "mekanism:module_attack_amplification_unit",
        "mekanism:module_farming_unit",
        "mekanism:module_shearing_unit",
        "mekanism:module_silk_touch_unit",
        "mekanism:module_fortune_unit",
        "mekanism:dimensional_stabilizer",
        "mekanism:quantum_entangloporter",
        "mekanism:hdpe_elytra",
        "bettercopper:copper_heart",
        "bettercopper:reversed_copper_heart",
        "mekanism:module_base",
        "mekanism:meka_tool",
        "mekanism:portable_teleporter",
        "mekanism:portable_qio_dashboard",
        "mekanism:canteen",
        "mekanism:creative_bin",

        // Occultism
        "occultism:storage_controller",
        "occultism:storage_stabilizer_tier1",
        "occultism:storage_stabilizer_tier2",
        "occultism:storage_stabilizer_tier3",
        "occultism:storage_stabilizer_tier4",
        "occultism:storage_remote_inert",
        "occultism:storage_remote",
        "occultism:storage_controller_base",
        "occultism:ritual_dummy/craft_stabilizer_tier1",
        "occultism:ritual_dummy/craft_stabilizer_tier2",
        "occultism:ritual_dummy/craft_stabilizer_tier3",
        "occultism:ritual_dummy/craft_stabilizer_tier4",
        "occultism:ritual_dummy/craft_storage_controller_base",
        "occultism:ritual_dummy/craft_storage_remote",
        "occultism:ritual_dummy/summon_djinni_manage_machine",
        "occultism:stable_wormhole",
        "occultism:ritual_dummy/craft_stable_wormhole",

        // Create Ender Transmission
        "createendertransmission:chunk_loader",

        // Create Jetpacks & Stuff & Additions
        "create_jetpack:netherite_jetpack",
        "create_jetpack:jetpack",
        "create_sa:brass_jetpack_chestplate",
        "create_sa:andesite_jetpack_chestplate",
        "create_sa:copper_jetpack_chestplate",
        "create_sa:netherite_jetpack_chestplate",
        "create_sa:andesite_exoskeleton_chestplate",
        "create_sa:brass_exoskeleton_chestplate",
        "create_sa:copper_exoskeleton_chestplate",
        "create_sa:block_picker",

        // Create Goggles
        "creategoggles:module_goggle_unit",

        // Sophisticated Backpacks
        "sophisticatedbackpacks:infinity_upgrade",
        "sophisticatedbackpacks:inception_upgrade",
        "sophisticatedbackpacks:stack_upgrade_omega_tier",

        // Sophisticated Storage
        "sophisticatedstorage:infinity_upgrade",
        "sophisticatedstorage:stack_upgrade_omega_tier",

        // ComputerCraft
        "computercraft:turtle_normal",
        "computercraft:turtle_advanced",

        // Ars Nouveau
        "ars_nouveau:planarium",

        // Supplementaries Cannon Boats (crash server)
        "supplementaries:cannon_boat_oak",
        "supplementaries:cannon_boat_spruce",
        "supplementaries:cannon_boat_birch",
        "supplementaries:cannon_boat_jungle",
        "supplementaries:cannon_boat_acacia",
        "supplementaries:cannon_boat_dark_oak",
        "supplementaries:cannon_boat_mangrove",
        "supplementaries:cannon_boat_cherry",
        "supplementaries:cannon_raft_bamboo",

        // Backtanks (Banned)
        "creategoggles:chainmail_backtank",
        "creategoggles:diamond_backtank",
        "creategoggles:golden_backtank",
        "creategoggles:iron_backtank",
        "creategoggles:leather_backtank",
        "create:netherite_backtank",

        // Easy Villagers (OP/exploit)
        "easy_villagers:iron_farm",

        // Advanced Peripherals (chunk loading exploit)
        "advancedperipherals:chunk_controller",

        // Ars Additions (server crash loop on use)
        "ars_additions:exploration_warp_scroll",

        // Aether (full invisibility even to spectators - staff cannot moderate)
        "aether:invisibility_cloak",
    ];

    hiddenItems.forEach((item) => event.remove(item));
});

// Also remove from their respective mod tabs
StartupEvents.modifyCreativeTab("mekanism:mekanism", (event) => {
    [
        "mekanism:atomic_disassembler", "mekanism:scuba_mask", "mekanism:scuba_tank",
        "mekanism:free_runners", "mekanism:free_runners_armored",
        "mekanism:jetpack", "mekanism:jetpack_armored",
        "mekanism:mekasuit_helmet", "mekanism:mekasuit_bodyarmor",
        "mekanism:mekasuit_pants", "mekanism:mekasuit_boots",
        "mekanism:flamethrower", "mekanism:electric_bow",
        "mekanism:module_color_modulation_unit", "mekanism:module_laser_dissipation_unit",
        "mekanism:module_radiation_shielding_unit", "mekanism:module_electrolytic_breathing_unit",
        "mekanism:module_inhalation_purification_unit", "mekanism:module_vision_enhancement_unit",
        "mekanism:module_nutritional_injection_unit", "mekanism:module_dosimeter_unit",
        "mekanism:module_geiger_unit", "mekanism:module_jetpack_unit",
        "mekanism:module_charge_distribution_unit", "mekanism:module_gravitational_modulating_unit",
        "mekanism:module_elytra_unit", "mekanism:module_locomotive_boosting_unit",
        "mekanism:module_gyroscopic_stabilization_unit", "mekanism:module_hydrostatic_repulsor_unit",
        "mekanism:module_motorized_servo_unit", "mekanism:module_hydraulic_propulsion_unit",
        "mekanism:module_magnetic_attraction_unit", "mekanism:module_frost_walker_unit",
        "mekanism:module_soul_surfer_unit", "mekanismgenerators:module_geothermal_generator_unit",
        "mekanismgenerators:module_solar_recharging_unit", "mekanism:module_teleportation_unit",
        "mekanism:module_vein_mining_unit", "mekanism:module_blasting_unit",
        "mekanism:module_energy_unit", "mekanism:module_excavation_escalation_unit",
        "mekanism:module_attack_amplification_unit", "mekanism:module_farming_unit",
        "mekanism:module_shearing_unit", "mekanism:module_silk_touch_unit",
        "mekanism:module_fortune_unit", "mekanism:dimensional_stabilizer",
        "mekanism:quantum_entangloporter", "mekanism:hdpe_elytra",
        "mekanism:module_base", "mekanism:meka_tool", "mekanism:portable_teleporter",
        "mekanism:portable_qio_dashboard",
        "mekanism:canteen", "mekanism:creative_bin", "mekanism:cardboard_box"
    ].forEach(item => event.remove(item));
});

StartupEvents.modifyCreativeTab("biomesoplenty:main", (event) => {
    ["biomesoplenty:anomaly", "biomesoplenty:unmapped_end_stone", "biomesoplenty:null_block",
     "biomesoplenty:null_leaves", "biomesoplenty:null_plant", "biomesoplenty:liquid_null_bucket"
    ].forEach(item => event.remove(item));
});

StartupEvents.modifyCreativeTab("dndecor:dndecor_tab", (event) => {
    const dndecorItems = [
        "dndecor:andesite_cross_bolt", "dndecor:andesite_dash_bolt", "dndecor:andesite_dot_bolt", "dndecor:andesite_flat_bolt",
        "dndecor:brass_cross_bolt", "dndecor:brass_dash_bolt", "dndecor:brass_dot_bolt", "dndecor:brass_flat_bolt",
        "dndecor:copper_cross_bolt", "dndecor:copper_dash_bolt", "dndecor:copper_dot_bolt", "dndecor:copper_flat_bolt",
        "dndecor:gold_cross_bolt", "dndecor:gold_dash_bolt", "dndecor:gold_dot_bolt", "dndecor:gold_flat_bolt",
        "dndecor:industrial_cross_bolt", "dndecor:industrial_dash_bolt", "dndecor:industrial_dot_bolt", "dndecor:industrial_flat_bolt",
        "dndecor:iron_cross_bolt", "dndecor:iron_dash_bolt", "dndecor:iron_dot_bolt", "dndecor:iron_flat_bolt",
        "dndecor:netherite_cross_bolt", "dndecor:netherite_dash_bolt", "dndecor:netherite_dot_bolt", "dndecor:netherite_flat_bolt",
        "dndecor:zinc_cross_bolt", "dndecor:zinc_dash_bolt", "dndecor:zinc_dot_bolt", "dndecor:zinc_flat_bolt"
    ];
    dndecorItems.forEach(item => event.remove(item));
});

StartupEvents.modifyCreativeTab("computercraft:main", (event) => {
    ["computercraft:turtle_normal", "computercraft:turtle_advanced"].forEach(item => event.remove(item));
});

StartupEvents.modifyCreativeTab("creategoggles:main", (event) => {
    ["creategoggles:module_goggle_unit", "creategoggles:chainmail_backtank", "creategoggles:diamond_backtank",
     "creategoggles:golden_backtank", "creategoggles:iron_backtank", "creategoggles:leather_backtank"
    ].forEach(item => event.remove(item));
});

StartupEvents.modifyCreativeTab("sophisticatedbackpacks:backpacks", (event) => {
    ["sophisticatedbackpacks:infinity_upgrade", "sophisticatedbackpacks:inception_upgrade",
     "sophisticatedbackpacks:stack_upgrade_omega_tier"
    ].forEach(item => event.remove(item));
});

StartupEvents.modifyCreativeTab("sophisticatedstorage:storage", (event) => {
    ["sophisticatedstorage:infinity_upgrade", "sophisticatedstorage:stack_upgrade_omega_tier"
    ].forEach(item => event.remove(item));
});

StartupEvents.modifyCreativeTab("occultism:occultism", (event) => {
    ["occultism:storage_controller", "occultism:storage_stabilizer_tier1",
     "occultism:storage_stabilizer_tier2", "occultism:storage_stabilizer_tier3",
     "occultism:storage_stabilizer_tier4", "occultism:storage_remote_inert",
     "occultism:storage_remote", "occultism:storage_controller_base",
     "occultism:ritual_dummy/craft_stabilizer_tier1", "occultism:ritual_dummy/craft_stabilizer_tier2",
     "occultism:ritual_dummy/craft_stabilizer_tier3", "occultism:ritual_dummy/craft_stabilizer_tier4",
     "occultism:ritual_dummy/craft_storage_controller_base", "occultism:ritual_dummy/craft_storage_remote",
     "occultism:ritual_dummy/summon_djinni_manage_machine",
     "occultism:stable_wormhole", "occultism:ritual_dummy/craft_stable_wormhole"
    ].forEach(item => event.remove(item));
});

StartupEvents.modifyCreativeTab("createendertransmission:main", (event) => {
    event.remove("createendertransmission:chunk_loader");
});

StartupEvents.modifyCreativeTab("create_jetpack:main", (event) => {
    ["create_jetpack:netherite_jetpack", "create_jetpack:jetpack"].forEach(item => event.remove(item));
});

StartupEvents.modifyCreativeTab("create_sa:main", (event) => {
    ["create_sa:brass_jetpack_chestplate", "create_sa:andesite_jetpack_chestplate",
     "create_sa:copper_jetpack_chestplate", "create_sa:netherite_jetpack_chestplate",
     "create_sa:andesite_exoskeleton_chestplate", "create_sa:brass_exoskeleton_chestplate",
     "create_sa:copper_exoskeleton_chestplate", "create_sa:block_picker"
    ].forEach(item => event.remove(item));
});

// Ars Nouveau
StartupEvents.modifyCreativeTab("ars_nouveau:ars_nouveau", (event) => {
    event.remove("ars_nouveau:planarium");
});

// BetterCopper
StartupEvents.modifyCreativeTab("bettercopper:bettercopper", (event) => {
    ["bettercopper:copper_heart", "bettercopper:reversed_copper_heart"].forEach(item => event.remove(item));
});

// Create (Backtanks)
StartupEvents.modifyCreativeTab("create:base", (event) => {
    ["create:netherite_backtank"].forEach(item => event.remove(item));
});

// Easy Villagers (OP/exploit)
StartupEvents.modifyCreativeTab("easy_villagers:tab", (event) => {
    event.remove("easy_villagers:iron_farm");
});

// Supplementaries (Cannon Boats - crash server)
StartupEvents.modifyCreativeTab("supplementaries:tab", (event) => {
    ["supplementaries:cannon_boat_oak", "supplementaries:cannon_boat_spruce",
     "supplementaries:cannon_boat_birch", "supplementaries:cannon_boat_jungle",
     "supplementaries:cannon_boat_acacia", "supplementaries:cannon_boat_dark_oak",
     "supplementaries:cannon_boat_mangrove", "supplementaries:cannon_boat_cherry",
     "supplementaries:cannon_raft_bamboo"
    ].forEach(item => event.remove(item));
});
