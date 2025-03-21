import React from 'react';

// 根据武器等级定义对应的颜色类名（Tailwind CSS 类名）
const levelColors = {
  "普通": "text-white",
  "稀有": "text-sky-500",
  "神器": "text-pink-500",
  "传说": "text-orange-500",
  "史诗": "text-yellow-500"
};

function WeaponCard({ weapon }) {
  // 获取对应等级的颜色类名，若不存在则使用默认颜色
  const colorClass = levelColors[weapon.level] || levelColors[weapon.color];

  return (
    <div className="border p-4 rounded shadow-md">
      <div className="flex items-center justify-between">
        <h3 className={`text-xl font-bold ${colorClass}`}>
          {weapon.name} ({weapon.type})
        </h3>
        {weapon.level && (
          <span className={`font-bold ${colorClass}`}>
            {weapon.level}
          </span>
        )}
      </div>
      <div className="mt-2">
        <strong>属性:</strong>
        <div>
          {weapon.attributes && weapon.attributes.length > 0 ? (
            weapon.attributes.map((attr, index) => (
              <div key={index}>
                {attr.name}: {attr.value}
              </div>
            ))
          ) : (
            <div>无属性数据</div>
          )}
        </div>
        {weapon.mainAttribute && (
          <div>
            <strong>主要属性:</strong> {weapon.mainAttribute}
          </div>
        )}
      </div>
      {weapon.specialEffects && (
        <div className="mt-2">
          <strong>特效:</strong>
          <div>
            {weapon.specialEffects && weapon.specialEffects.length > 0 ? (
              weapon.specialEffects.map((attr, index) => (
                <div key={index}>
                  {attr.name}: {attr.value}
                </div>
              ))
            ) : (
              <div>无属性数据</div>
            )}
          </div>
        </div>
      )}
      {weapon.specialSkills && (
        <div className="mt-2">
          <strong>特技:</strong>
          <div>
            {weapon.specialSkills && weapon.specialSkills.length > 0 ? (
                weapon.specialSkills.map((attr, index) => (
                  <div key={index}>
                    {attr.name}: {attr.value}
                  </div>
                ))
              ) : (
                <div>无属性数据</div>
              )}
          </div>
        </div>
      )}
      <div className="mt-2">
        <strong>描述:</strong>
        <p>{weapon.description}</p>
      </div>
      <div className="mt-2">
        <strong>背景:</strong>
        <p>{weapon.background}</p>
      </div>
      {weapon.part && (
        <div className="mt-2">
          <strong>部位:</strong>
          <p>{weapon.part}</p>
        </div>
      )}
    </div>
  );
}

export default WeaponCard;
