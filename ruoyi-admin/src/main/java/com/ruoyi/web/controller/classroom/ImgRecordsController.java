package com.ruoyi.web.controller.classroom;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.system.domain.ImgRecords;
import com.ruoyi.system.mapper.ImgRecordsMapper;
import org.springframework.web.bind.annotation.*;

import jakarta.annotation.Resource;

/**
 * 图片检测记录控制器
 * 
 * @author ruoyi
 */
@RestController
@RequestMapping("/imgRecords")
public class ImgRecordsController {
    
    @Resource
    private ImgRecordsMapper imgRecordsMapper;

    /**
     * 获取所有记录
     */
    @GetMapping("/all")
    public AjaxResult GetAll() {
        return AjaxResult.success(imgRecordsMapper.selectList(null));
    }

    /**
     * 根据ID获取记录
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable int id) {
        return AjaxResult.success(imgRecordsMapper.selectById(id));
    }

    /**
     * 分页查询
     */
    @GetMapping
    public AjaxResult findPage(@RequestParam(defaultValue = "1") Integer pageNum,
                              @RequestParam(defaultValue = "10") Integer pageSize,
                              @RequestParam(defaultValue = "") String search,
                              @RequestParam(defaultValue = "") String search1,
                              @RequestParam(defaultValue = "") String search3,
                              @RequestParam(defaultValue = "") String search2) {
        LambdaQueryWrapper<ImgRecords> wrapper = Wrappers.<ImgRecords>lambdaQuery();
        wrapper.orderByDesc(ImgRecords::getStartTime);
        if (StringUtils.isNotBlank(search)) {
            wrapper.like(ImgRecords::getUsername, search);
        }
        if (StringUtils.isNotBlank(search1)) {
            wrapper.like(ImgRecords::getStartTime, search1);
        }
        if (StringUtils.isNotBlank(search2)) {
            wrapper.like(ImgRecords::getLabel, search2);
        }
        if (StringUtils.isNotBlank(search3)) {
            wrapper.like(ImgRecords::getConf, search3);
        }
        Page<ImgRecords> page = imgRecordsMapper.selectPage(new Page<>(pageNum, pageSize), wrapper);
        return AjaxResult.success(page);
    }

    /**
     * 删除记录（支持单个和批量删除）
     */
    @DeleteMapping("/delete/{ids}")
    public AjaxResult delete(@PathVariable String ids) {
        if (ids.contains(",")) {
            // 批量删除
            String[] idArray = ids.split(",");
            for (String id : idArray) {
                imgRecordsMapper.deleteById(Integer.parseInt(id.trim()));
            }
        } else {
            // 单个删除
            imgRecordsMapper.deleteById(Integer.parseInt(ids));
        }
        return AjaxResult.success();
    }

    /**
     * 更新记录
     */
    @PutMapping("/updates")
    public AjaxResult updates(@RequestBody ImgRecords imgrecords) {
        imgRecordsMapper.updateById(imgrecords);
        return AjaxResult.success();
    }

    /**
     * 保存记录
     */
    @PostMapping("/save")
    public AjaxResult save(@RequestBody ImgRecords imgrecords) {
        imgRecordsMapper.insert(imgrecords);
        return AjaxResult.success();
    }
}

