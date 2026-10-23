const AVATAR_IMAGES = {
  avatar_1: "/CACHORROBOLA.png",
  avatar_2: "/GATOBOLA.png",
  avatar_3: "/SAPOBOLA.png",
  avatar_4: "/GAZELABOLA.png",
};

const AVATAR_PORTRAIT_IMAGES = {
  avatar_1: "/DOGBG.jpeg",
  avatar_2: "/GATOBG.jpeg",
  avatar_3: "/SAPOBG.jpeg",
  avatar_4: "/GAZELABG.jpeg",
};

export function getAvatarImage(avatarId) {
  return AVATAR_IMAGES[String(avatarId ?? "avatar_3").toLowerCase()] ?? "/SAPOBOLA.png";
}

export function getAvatarPortraitImage(avatarId) {
  return AVATAR_PORTRAIT_IMAGES[String(avatarId ?? "avatar_3").toLowerCase()] ?? "/SAPOBG.jpeg";
}
