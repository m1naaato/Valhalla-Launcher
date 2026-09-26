// Priority: 950
/*
    Custom Armor Materials for Arcadia V2
    Registered via StartupEvents.registry('armor_material')
    Author: vyrriox
*/

StartupEvents.registry('armor_material', event => {
    // Adept Armor Material - Cultist/Sect
    event.create('arcadia:adept')
        .defense({ BOOTS: 2, LEGGINGS: 5, CHESTPLATE: 6, HELMET: 2, BODY: 5 })
        .enchantmentValue(15)
        .toughness(1.0)
        .knockbackResistance(0.05)

    // Heretic Armor Material - Rebel cult
    event.create('arcadia:heretic')
        .defense({ BOOTS: 2, LEGGINGS: 5, CHESTPLATE: 6, HELMET: 2, BODY: 5 })
        .enchantmentValue(15)
        .toughness(1.0)
        .knockbackResistance(0.05)
})
