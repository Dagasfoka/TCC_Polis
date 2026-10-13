const AVATAR_IMAGES = {
  avatar_1: "/CACHORROBOLA.png",
  avatar_2: "/GATOBOLA.png",
  avatar_3: "/SAPOBOLA.png",
  avatar_4: "/GAZELABOLA.png",
};

export function getAvatarImage(avatarId) {
  return AVATAR_IMAGES[String(avatarId ?? "avatar_3").toLowerCase()] ?? "/SAPOBOLA.png";
}
